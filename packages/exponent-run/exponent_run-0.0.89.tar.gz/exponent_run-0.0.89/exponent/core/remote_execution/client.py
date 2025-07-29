from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any, Optional, TypeVar, Union, Dict, cast

from dataclasses import dataclass
from exponent.core.config import is_editable_install
from exponent.core.remote_execution.error_info import serialize_error_info
from exponent.core.remote_execution.types import ChatSource
from exponent.core.types.event_types import (
    CodeBlockEvent,
    CommandEvent,
    FileWriteEvent,
    LocalEventType,
)
from exponent.utils.version import get_installed_version
import websockets.client
import websockets.exceptions
from httpx import (
    AsyncClient,
    codes as http_status,
)
from pydantic import BaseModel

from exponent.commands.utils import ConnectionTracker
from exponent.core.remote_execution import files, system_context
from exponent.core.remote_execution.code_execution import (
    execute_code,
    execute_code_streaming,
)
from exponent.core.remote_execution.command_execution import execute_command
from exponent.core.remote_execution.file_write import execute_file_write
from exponent.core.remote_execution.session import (
    RemoteExecutionClientSession,
    get_session,
)
from exponent.core.remote_execution.checkpoints import (
    create_checkpoint,
    rollback_to_checkpoint,
)
from exponent.core.remote_execution.types import (
    CLIConnectedState,
    CodeExecutionRequest,
    StreamingCodeExecutionRequest,
    CommandRequest,
    CreateChatResponse,
    ExecutionEndResponse,
    FileWriteRequest,
    GetAllTrackedFilesRequest,
    GetFileAttachmentRequest,
    GetFileAttachmentsRequest,
    GetMatchingFilesRequest,
    HaltRequest,
    HaltResponse,
    HeartbeatInfo,
    ListFilesRequest,
    RemoteExecutionRequestType,
    RemoteExecutionResponseType,
    RunWorkflowRequest,
    StartChatRequest,
    StartChatResponse,
    SwitchCLIChatRequest,
    SwitchCLIChatResponse,
    SystemContextRequest,
    ErrorResponse,
    CreateCheckpointRequest,
    RollbackToCheckpointRequest,
)
from exponent.core.remote_execution.utils import (
    convert_event_to_execution_request,
    deserialize_api_response,
    deserialize_request_data,
    serialize_message,
)

logger = logging.getLogger(__name__)


TModel = TypeVar("TModel", bound=BaseModel)


@dataclass
class WSDisconnected:
    error_message: Optional[str] = None


@dataclass
class SwitchCLIChat:
    new_chat_uuid: str


REMOTE_EXECUTION_CLIENT_EXIT_INFO = Union[WSDisconnected, SwitchCLIChat]


class RemoteExecutionClient:
    def __init__(
        self,
        session: RemoteExecutionClientSession,
        file_cache: Optional[files.FileCache] = None,
    ):
        self.current_session = session
        self.file_cache = file_cache or files.FileCache(session.working_directory)

        # for active code executions, track whether they should be halted
        # correlation_id -> should_halt
        self._halt_states: Dict[str, bool] = {}
        self._halt_lock = asyncio.Lock()

    @property
    def working_directory(self) -> str:
        return self.current_session.working_directory

    @property
    def api_client(self) -> AsyncClient:
        return self.current_session.api_client

    @property
    def ws_client(self) -> AsyncClient:
        return self.current_session.ws_client

    async def add_code_execution_to_halt_states(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states[correlation_id] = False

    async def halt_all_code_executions(self) -> None:
        async with self._halt_lock:
            self._halt_states = {
                correlation_id: True for correlation_id in self._halt_states.keys()
            }

    async def clear_halt_state(self, correlation_id: str) -> None:
        async with self._halt_lock:
            self._halt_states.pop(correlation_id, None)

    def get_halt_check(self, correlation_id: str) -> Callable[[], bool]:
        def should_halt() -> bool:
            # Don't need to lock here, since just reading from dict
            return self._halt_states.get(correlation_id, False)

        return should_halt

    async def _handle_websocket_message(
        self,
        msg: str,
        websocket: websockets.client.WebSocketClientProtocol,
        requests: asyncio.Queue[RemoteExecutionRequestType],
    ) -> Optional[REMOTE_EXECUTION_CLIENT_EXIT_INFO]:
        """Handle an incoming websocket message.
        Returns None to continue processing, or a REMOTE_EXECUTION_CLIENT_EXIT_INFO to exit."""

        msg_data = json.loads(msg)
        if msg_data["type"] != "request":
            return None

        data = json.dumps(msg_data["data"])
        request = deserialize_request_data(data)

        if isinstance(request, HaltRequest):
            logger.debug(
                f"Received HaltRequest for correlation_id {request.correlation_id}"
            )
            await self.halt_all_code_executions()
            data = json.loads(
                serialize_message(
                    HaltResponse(
                        correlation_id=request.correlation_id,
                    )
                )
            )
            msg = json.dumps({"type": "result", "data": data})
            logger.debug(
                f"Sending HaltResponse for correlation_id {request.correlation_id}"
            )
            await websocket.send(msg)
            return None

        elif isinstance(request, SwitchCLIChatRequest):
            data = json.loads(
                serialize_message(
                    SwitchCLIChatResponse(
                        correlation_id=request.correlation_id,
                    )
                )
            )
            msg = json.dumps({"type": "result", "data": data})
            await websocket.send(msg)
            return SwitchCLIChat(new_chat_uuid=request.new_chat_uuid)

        elif isinstance(request, (CodeExecutionRequest, StreamingCodeExecutionRequest)):
            await self.add_code_execution_to_halt_states(request.correlation_id)
            await requests.put(request)
            return None

        else:
            await requests.put(request)
            return None

    async def _setup_tasks(
        self,
        beats: asyncio.Queue[HeartbeatInfo],
        requests: asyncio.Queue[RemoteExecutionRequestType],
        results: asyncio.Queue[RemoteExecutionResponseType],
    ) -> list[asyncio.Task[None]]:
        """Setup heartbeat and executor tasks."""

        async def beat() -> None:
            while True:
                info = await self.get_heartbeat_info()
                await beats.put(info)
                await asyncio.sleep(3)

        # Lock to ensure that only one executor can grab a
        # request at a time.
        requests_lock = asyncio.Lock()

        # Lock to ensure that only one executor can put a
        # result in the results queue at a time.
        results_lock = asyncio.Lock()

        async def executor() -> None:
            # We use locks here to protect the request/result
            # queues from being accessed by multiple executors.
            while True:
                async with requests_lock:
                    request = await requests.get()

                try:
                    if isinstance(request, StreamingCodeExecutionRequest):
                        async for streaming_response in self.handle_streaming_request(
                            request
                        ):
                            async with results_lock:
                                await results.put(streaming_response)
                    else:
                        # Note that we don't want to hold the lock here
                        # because we want other executors to be able to
                        # grab requests while we're handling a request.
                        response = await self.handle_request(request)
                        async with results_lock:
                            await results.put(response)
                except Exception as e:
                    logger.info(f"Error handling request {request.namespace}:\n\n{e}")
                    async with results_lock:
                        await results.put(
                            ErrorResponse(
                                error_type="request_error",
                                correlation_id=request.correlation_id,
                                request_namespace=request.namespace,
                                error_info=serialize_error_info(e),
                            )
                        )

        beat_task = asyncio.create_task(beat())
        # Three parallel executors to handle requests

        executor_tasks = [
            asyncio.create_task(executor()),
            asyncio.create_task(executor()),
            asyncio.create_task(executor()),
        ]

        return [beat_task] + executor_tasks

    async def _process_websocket_messages(
        self,
        websocket: websockets.client.WebSocketClientProtocol,
        beats: asyncio.Queue[HeartbeatInfo],
        requests: asyncio.Queue[RemoteExecutionRequestType],
        results: asyncio.Queue[RemoteExecutionResponseType],
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
        """Process messages from the websocket connection."""
        try:
            recv = asyncio.create_task(websocket.recv())
            get_beat = asyncio.create_task(beats.get())
            get_result = asyncio.create_task(results.get())
            pending = {recv, get_beat, get_result}

            while True:
                done, pending = await asyncio.wait(
                    pending, return_when=asyncio.FIRST_COMPLETED
                )

                if recv in done:
                    msg = str(recv.result())
                    exit_info = await self._handle_websocket_message(
                        msg, websocket, requests
                    )
                    if exit_info is not None:
                        return exit_info

                    recv = asyncio.create_task(websocket.recv())
                    pending.add(recv)

                if get_beat in done:
                    info = get_beat.result()
                    data = json.loads(info.model_dump_json())
                    msg = json.dumps({"type": "heartbeat", "data": data})
                    await websocket.send(msg)

                    get_beat = asyncio.create_task(beats.get())
                    pending.add(get_beat)

                if get_result in done:
                    response = get_result.result()
                    data = json.loads(serialize_message(response))
                    msg = json.dumps({"type": "result", "data": data})
                    await websocket.send(msg)

                    get_result = asyncio.create_task(results.get())
                    pending.add(get_result)
        finally:
            for task in pending:
                task.cancel()

            await asyncio.gather(*pending, return_exceptions=True)

    async def _handle_websocket_connection(
        self,
        websocket: websockets.client.WebSocketClientProtocol,
        connection_tracker: Optional[ConnectionTracker],
    ) -> Optional[REMOTE_EXECUTION_CLIENT_EXIT_INFO]:
        """Handle a single websocket connection.
        Returns None to continue with reconnection attempts, or an exit info to terminate."""
        if connection_tracker is not None:
            await connection_tracker.set_connected(True)

        beats: asyncio.Queue[HeartbeatInfo] = asyncio.Queue()
        requests: asyncio.Queue[RemoteExecutionRequestType] = asyncio.Queue()
        results: asyncio.Queue[RemoteExecutionResponseType] = asyncio.Queue()

        tasks = await self._setup_tasks(beats, requests, results)

        try:
            return await self._process_websocket_messages(
                websocket, beats, requests, results
            )
        except websockets.exceptions.ConnectionClosed as e:
            if e.rcvd is not None:
                if e.rcvd.code == 1000:
                    # Normal closure, exit completely
                    return WSDisconnected()
                elif e.rcvd.code == 1008:
                    error_message = (
                        "Error connecting to websocket"
                        if e.rcvd.reason is None
                        else e.rcvd.reason
                    )
                    return WSDisconnected(error_message=error_message)
            # Otherwise, allow reconnection attempt
            return None
        except TimeoutError:
            # Timeout, allow reconnection attempt
            # TODO: investgate if this is needed, possibly scope it down
            return None
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            if connection_tracker is not None:
                await connection_tracker.set_connected(False)

    async def run_connection(
        self,
        chat_uuid: str,
        connection_tracker: Optional[ConnectionTracker] = None,
    ) -> REMOTE_EXECUTION_CLIENT_EXIT_INFO:
        """Run the websocket connection loop."""
        self.current_session.set_chat_uuid(chat_uuid)

        async for websocket in self.ws_connect(f"/api/ws/chat/{chat_uuid}"):
            result = await self._handle_websocket_connection(
                websocket, connection_tracker
            )
            if result is not None:
                return result
            # If we get None, we'll try to reconnect

        # If we exit the websocket connection loop without returning,
        # it means we couldn't establish a connection
        return WSDisconnected(error_message="Could not establish websocket connection")

    async def check_remote_end_event(self, chat_uuid: str) -> bool:
        response = await self.api_client.get(
            f"/api/remote_execution/{chat_uuid}/execution_end",
        )
        execution_end_response = await deserialize_api_response(
            response, ExecutionEndResponse
        )
        return execution_end_response.execution_ended

    async def create_chat(self, chat_source: ChatSource) -> CreateChatResponse:
        response = await self.api_client.post(
            "/api/remote_execution/create_chat",
            params={"chat_source": chat_source.value},
        )
        return await deserialize_api_response(response, CreateChatResponse)

    async def start_chat(self, chat_uuid: str, prompt: str) -> StartChatResponse:
        response = await self.api_client.post(
            "/api/remote_execution/start_chat",
            json=StartChatRequest(
                chat_uuid=chat_uuid,
                prompt=prompt,
            ).model_dump(),
            timeout=60,
        )
        return await deserialize_api_response(response, StartChatResponse)

    async def run_workflow(self, chat_uuid: str, workflow_id: str) -> dict[str, Any]:
        response = await self.api_client.post(
            "/api/remote_execution/run_workflow",
            json=RunWorkflowRequest(
                chat_uuid=chat_uuid,
                workflow_id=workflow_id,
            ).model_dump(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Failed to run workflow with status code {response.status_code} and response {response.text}"
            )
        return cast(dict[str, Any], response.json())

    async def get_heartbeat_info(self) -> HeartbeatInfo:
        return HeartbeatInfo(
            system_info=await system_context.get_system_info(self.working_directory),
            exponent_version=get_installed_version(),
            editable_installation=is_editable_install(),
        )

    async def send_heartbeat(self, chat_uuid: str) -> CLIConnectedState:
        logger.info(f"Sending heartbeat for chat_uuid {chat_uuid}")
        heartbeat_info = await self.get_heartbeat_info()
        response = await self.api_client.post(
            f"/api/remote_execution/{chat_uuid}/heartbeat",
            content=heartbeat_info.model_dump_json(),
            timeout=60,
        )
        if response.status_code != http_status.OK:
            raise Exception(
                f"Heartbeat failed with status code {response.status_code} and response {response.text}"
            )
        connected_state = await deserialize_api_response(response, CLIConnectedState)
        logger.info(f"Heartbeat response: {connected_state}")
        return connected_state

    async def handle_request(
        self, request: Union[RemoteExecutionRequestType, LocalEventType]
    ) -> RemoteExecutionResponseType:
        if isinstance(request, (CodeBlockEvent, FileWriteEvent, CommandEvent)):
            request = convert_event_to_execution_request(request)

        try:
            response: RemoteExecutionResponseType
            if isinstance(request, CodeExecutionRequest):
                response = await execute_code(
                    request,
                    self.current_session,
                    working_directory=self.working_directory,
                    should_halt=self.get_halt_check(request.correlation_id),
                )
            elif isinstance(request, FileWriteRequest):
                response = await execute_file_write(
                    request,
                    working_directory=self.working_directory,
                )
            elif isinstance(request, ListFilesRequest):
                response = await files.list_files(request)
            elif isinstance(request, GetFileAttachmentRequest):
                response = await files.get_file_attachment(
                    request, self.working_directory
                )
            elif isinstance(request, GetFileAttachmentsRequest):
                response = await files.get_file_attachments(
                    request, self.working_directory
                )
            elif isinstance(request, GetMatchingFilesRequest):
                response = await files.get_matching_files(request, self.file_cache)
            elif isinstance(request, SystemContextRequest):
                response = await system_context.get_system_context(
                    request, self.working_directory
                )
            elif isinstance(request, GetAllTrackedFilesRequest):
                response = await files.get_all_tracked_files(
                    request, self.working_directory
                )
            elif isinstance(request, CommandRequest):
                response = await execute_command(
                    request,
                    self.working_directory,
                )
            elif isinstance(request, StreamingCodeExecutionRequest):
                assert False, (
                    "CodeExecutionStreamingRequest should be sent to handle_streaming_request"
                )
            elif isinstance(request, HaltRequest):
                assert False, "HaltRequest should be handled in the main loop"
            elif isinstance(request, SwitchCLIChatRequest):
                assert False, "SwitchCLIChatRequest should be handled in the main loop"
            elif isinstance(request, CreateCheckpointRequest):
                response = await create_checkpoint(request)
            elif isinstance(request, RollbackToCheckpointRequest):
                response = await rollback_to_checkpoint(
                    request.correlation_id,
                    request.head_commit,
                    request.uncommitted_changes_commit,
                )
            else:
                logger.info(f"Unhandled request type: {type(request)}")
                response = ErrorResponse(
                    error_type="unknown_request_type",
                    correlation_id=request.correlation_id,
                    request_namespace=request.namespace,
                )
            return response
        finally:
            # Clean up halt state after request is complete
            if isinstance(request, CodeExecutionRequest) or isinstance(
                request, StreamingCodeExecutionRequest
            ):
                await self.clear_halt_state(request.correlation_id)

    async def handle_streaming_request(
        self, request: StreamingCodeExecutionRequest
    ) -> AsyncGenerator[RemoteExecutionResponseType, None]:
        if not isinstance(request, StreamingCodeExecutionRequest):
            assert False, f"{type(request)} should be sent to handle_streaming_request"
        async for output in execute_code_streaming(
            request,
            self.current_session,
            working_directory=self.working_directory,
            should_halt=self.get_halt_check(request.correlation_id),
        ):
            yield output

    def ws_connect(self, path: str) -> websockets.client.connect:
        base_url = (
            str(self.ws_client.base_url)
            .replace("http://", "ws://")
            .replace("https://", "wss://")
        )

        url = f"{base_url}{path}"
        headers = {"api-key": self.api_client.headers["api-key"]}

        conn = websockets.client.connect(
            url, extra_headers=headers, timeout=10, ping_timeout=10
        )

        # Stop exponential backoff from blowing up
        # the wait time between connection attempts
        conn.BACKOFF_MAX = 2
        conn.BACKOFF_INITIAL = 1  # pyright: ignore

        return conn

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str,
        base_url: str,
        base_ws_url: str,
        working_directory: str,
        file_cache: Optional[files.FileCache] = None,
    ) -> AsyncGenerator[RemoteExecutionClient, None]:
        async with get_session(
            working_directory, base_url, base_ws_url, api_key
        ) as session:
            yield RemoteExecutionClient(session, file_cache)
