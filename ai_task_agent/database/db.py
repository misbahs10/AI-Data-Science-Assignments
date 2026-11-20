
import sqlite3
from pathlib import Path

# Database project ke database folder mein create hogi
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"


def get_connection():
    """SQLite database connection return karta hai."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Tasks table create karta hai agar pehle se exist na karti ho."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                due_date TEXT DEFAULT '',
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()


def create_task(title, description="", due_date="", priority="Medium"):
    """Database mein naya task save karta hai."""
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty.")

    if priority not in ("Low", "Medium", "High"):
        raise ValueError("Priority must be Low, Medium, or High.")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, description, due_date, priority)
            VALUES (?, ?, ?, ?)
            """,
            (title.strip(), description.strip(), due_date, priority)
        )
        connection.commit()
        return cursor.lastrowid


def get_tasks(status=None):
    """Tamam tasks ya selected status ke tasks return karta hai."""
    with get_connection() as connection:
        if status:
            rows = connection.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY id DESC",
                (status,)
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            ).fetchall()

        return [dict(row) for row in rows]


def complete_task(task_id):
    """Task ka status Completed karta hai."""
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE tasks SET status = 'Completed' WHERE id = ?",
            (task_id,)
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_task(task_id):
    """Task ko database se delete karta hai."""
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        connection.commit()
        return cursor.rowcount > 0


def get_task_summary():
    """Task statistics return karta hai."""
    with get_connection() as connection:
        row = connection.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending,
                SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed
            FROM tasks
        """).fetchone()

        return {
            "total": row["total"] or 0,
            "pending": row["pending"] or 0,
            "completed": row["completed"] or 0
        }


# Database initialize
initialize_database()
