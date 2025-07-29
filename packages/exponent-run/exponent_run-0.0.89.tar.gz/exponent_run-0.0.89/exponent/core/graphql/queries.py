EVENTS_FOR_CHAT_QUERY: str = """query EventsForChat($chatUuid: UUID!) {
  eventsForChat(chatUuid: $chatUuid) {
    ... on EventHistory {
      events {
        ... on GraphExponentEvent {
          eventUuid
        }
        ... on CheckpointCreatedEvent {
          __typename
          chatUuid
          parentUuid
          commitHash
          commitMessage
          gitMetadata
        }
      }
    }
  }
}
"""
