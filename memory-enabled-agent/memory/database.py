
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DATABASE_PATH


# ==========================================
# DATABASE CONNECTION
# ==========================================

@contextmanager
def get_connection():
    """
    Create a database connection.

    Automatically commits successful transactions,
    rolls back failed transactions and closes connection.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# UTILITY FUNCTIONS
# ==========================================

def get_current_time():
    """Return current UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def initialize_database():
    """
    Initialize database tables and indexes.

    Also migrates existing databases by adding
    the embedding column when it is missing.
    """

    with get_connection() as connection:

        # Conversations table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL
                    DEFAULT 'New Conversation',

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL

            )
        """)

        # Messages table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                conversation_id INTEGER NOT NULL,

                role TEXT NOT NULL
                    CHECK(role IN ('user', 'assistant')),

                content TEXT NOT NULL,

                created_at TEXT NOT NULL,

                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE

            )
        """)

        # Long-term memories table
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                memory TEXT NOT NULL,

                category TEXT NOT NULL
                    DEFAULT 'general',

                embedding TEXT,

                created_at TEXT NOT NULL,

                updated_at TEXT NOT NULL

            )
        """)

        # ======================================
        # DATABASE MIGRATIONS
        # ======================================

        columns = connection.execute(
            "PRAGMA table_info(memories)"
        ).fetchall()

        column_names = [
            column["name"]
            for column in columns
        ]

        if "embedding" not in column_names:

            connection.execute("""
                ALTER TABLE memories
                ADD COLUMN embedding TEXT
            """)

            print("Migration completed: embedding column added.")

        # ======================================
        # DATABASE INDEXES
        # ======================================

        connection.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_messages_conversation

            ON messages(conversation_id)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_memories_category

            ON memories(category)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_conversations_updated

            ON conversations(updated_at)
        """)

    print("Database initialized successfully!")


# ==========================================
# CONVERSATION MANAGEMENT
# ==========================================

def create_conversation(title="New Conversation"):
    """Create a new conversation."""

    title = title.strip()

    if not title:
        title = "New Conversation"

    current_time = get_current_time()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO conversations
            (title, created_at, updated_at)

            VALUES (?, ?, ?)
            """,
            (title, current_time, current_time)
        )

        return cursor.lastrowid


def get_conversations():
    """Retrieve all conversations."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM conversations

            ORDER BY updated_at DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]


def delete_conversation(conversation_id):
    """Delete a conversation and its messages."""

    with get_connection() as connection:

        cursor = connection.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        return cursor.rowcount > 0


# ==========================================
# MESSAGE MANAGEMENT
# ==========================================

def save_message(conversation_id, role, content):
    """Save a user or assistant message."""

    if role not in ("user", "assistant"):
        raise ValueError(
            "Role must be either 'user' or 'assistant'."
        )

    if not isinstance(content, str) or not content.strip():
        raise ValueError("Message content cannot be empty.")

    current_time = get_current_time()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO messages
            (conversation_id, role, content, created_at)

            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content.strip(),
                current_time
            )
        )

        connection.execute(
            """
            UPDATE conversations

            SET updated_at = ?

            WHERE id = ?
            """,
            (current_time, conversation_id)
        )

        return cursor.lastrowid


def get_messages(conversation_id):
    """Retrieve all messages from a conversation."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT id, conversation_id, role, content, created_at

            FROM messages

            WHERE conversation_id = ?

            ORDER BY id ASC
            """,
            (conversation_id,)
        ).fetchall()

        return [dict(row) for row in rows]


# ==========================================
# LONG-TERM MEMORY MANAGEMENT
# ==========================================

def save_memory(memory, category="general"):
    """Save information in long-term memory."""

    if not isinstance(memory, str) or not memory.strip():
        raise ValueError("Memory cannot be empty.")

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Memory category cannot be empty.")

    current_time = get_current_time()

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO memories

            (memory, category, embedding, created_at, updated_at)

            VALUES (?, ?, NULL, ?, ?)
            """,
            (
                memory.strip(),
                category.strip().lower(),
                current_time,
                current_time
            )
        )

        return cursor.lastrowid


def get_memories(category=None):
    """Retrieve all memories or memories by category."""

    with get_connection() as connection:

        if category:

            rows = connection.execute(
                """
                SELECT *

                FROM memories

                WHERE category = ?

                ORDER BY updated_at DESC
                """,
                (category.strip().lower(),)
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT *

                FROM memories

                ORDER BY updated_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]


def update_memory(memory_id, new_memory, category=None):
    """
    Update an existing memory.

    Old embedding is cleared because updated text
    requires a newly generated embedding.
    """

    if not isinstance(new_memory, str) or not new_memory.strip():
        raise ValueError("Memory cannot be empty.")

    current_time = get_current_time()

    with get_connection() as connection:

        if category is None:

            cursor = connection.execute(
                """
                UPDATE memories

                SET memory = ?,
                    embedding = NULL,
                    updated_at = ?

                WHERE id = ?
                """,
                (
                    new_memory.strip(),
                    current_time,
                    memory_id
                )
            )

        else:

            if not category.strip():
                raise ValueError("Category cannot be empty.")

            cursor = connection.execute(
                """
                UPDATE memories

                SET memory = ?,
                    category = ?,
                    embedding = NULL,
                    updated_at = ?

                WHERE id = ?
                """,
                (
                    new_memory.strip(),
                    category.strip().lower(),
                    current_time,
                    memory_id
                )
            )

        return cursor.rowcount > 0


def delete_memory(memory_id):
    """Delete a specific long-term memory."""

    with get_connection() as connection:

        cursor = connection.execute(
            """
            DELETE FROM memories

            WHERE id = ?
            """,
            (memory_id,)
        )

        return cursor.rowcount > 0


def get_memory_count():
    """Return total number of saved memories."""

    with get_connection() as connection:

        result = connection.execute(
            """
            SELECT COUNT(*) AS total

            FROM memories
            """
        ).fetchone()

        return result["total"]
