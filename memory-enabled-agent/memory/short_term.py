
from memory.database import (
    get_connection,
    save_message
)

from config import MAX_SHORT_TERM_MESSAGES


class ShortTermMemory:
    """Manage recent conversation context."""

    def __init__(self, max_messages=None):

        self.max_messages = (
            max_messages
            if max_messages is not None
            else MAX_SHORT_TERM_MESSAGES
        )

        if self.max_messages < 1:
            raise ValueError("max_messages must be at least 1.")

    def add_message(self, conversation_id, role, content):
        """Save a new conversation message."""

        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")

        save_message(
            conversation_id,
            role,
            content.strip()
        )

    def get_context(self, conversation_id):
        """Retrieve the most recent messages for LLM context."""

        with get_connection() as connection:

            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, self.max_messages)
            ).fetchall()

        # Reverse to maintain chronological order
        messages = [
            {
                "role": row["role"],
                "content": row["content"]
            }
            for row in reversed(rows)
        ]

        return messages

    def get_context_count(self, conversation_id):
        """Return the number of messages in current context."""

        return len(self.get_context(conversation_id))

    def clear_context(self, conversation_id):
        """
        Clear conversation messages.

        Note: This permanently deletes messages
        from the database, not just the LLM context.
        """

        with get_connection() as connection:

            connection.execute(
                """
                DELETE FROM messages
                WHERE conversation_id = ?
                """,
                (conversation_id,)
            )
