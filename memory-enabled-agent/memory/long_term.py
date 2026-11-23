
from memory.database import (
    save_memory,
    get_memories,
    update_memory,
    delete_memory,
    get_connection
)


class LongTermMemory:
    """Manage persistent user memories."""

    def add_memory(self, memory, category="general"):
        """Save a new memory and return its ID."""

        if not isinstance(memory, str) or not memory.strip():
            raise ValueError("Memory cannot be empty.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Memory category cannot be empty.")

        memory = memory.strip()
        category = category.strip().lower()

        # Avoid saving exact duplicate memories.
        with get_connection() as connection:

            existing = connection.execute(
                """
                SELECT id
                FROM memories
                WHERE LOWER(TRIM(memory)) = LOWER(?)
                AND category = ?
                """,
                (memory, category)
            ).fetchone()

            if existing:
                return existing["id"]

        return save_memory(memory, category)

    def get_all_memories(self):
        """Retrieve all saved memories."""

        return get_memories()

    def get_memories_by_category(self, category):
        """Retrieve memories from a specific category."""

        return get_memories(category)

    def search_memories(self, keyword):
        """Search memories using a keyword."""

        if not isinstance(keyword, str):
            return []

        keyword = keyword.strip()

        if not keyword:
            return []

        with get_connection() as connection:

            rows = connection.execute(
                """
                SELECT *
                FROM memories
                WHERE memory LIKE ? COLLATE NOCASE
                   OR category LIKE ? COLLATE NOCASE
                ORDER BY updated_at DESC
                """,
                (f"%{keyword}%", f"%{keyword}%")
            ).fetchall()

            return [dict(row) for row in rows]

    def update_existing_memory(
        self,
        memory_id,
        new_memory,
        category=None
    ):
        """Update an existing memory and return success status."""

        return update_memory(
            memory_id,
            new_memory,
            category
        )

    def delete_existing_memory(self, memory_id):
        """Delete a saved memory and return success status."""

        return delete_memory(memory_id)

    def get_memory_count(self):
        """Return total number of saved memories."""

        return len(self.get_all_memories())
