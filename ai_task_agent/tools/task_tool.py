
from database.db import (
    create_task as db_create_task,
    get_tasks as db_get_tasks,
    complete_task as db_complete_task,
    delete_task as db_delete_task,
    get_task_summary
)


def create_task(title, description="", due_date="", priority="Medium"):
    """Naya task create karta hai."""
    try:
        task_id = db_create_task(
            title, description, due_date, priority
        )
        return f"Task created successfully. Task ID: {task_id}"
    except (ValueError, Exception) as error:
        return f"Could not create task: {error}"


def list_tasks(status=None):
    """Tasks ki list return karta hai."""
    tasks = db_get_tasks(status)

    if not tasks:
        return "No tasks found."

    return "\n".join(
        [
            f"ID: {task['id']} | Title: {task['title']} | "
            f"Priority: {task['priority']} | Status: {task['status']} | "
            f"Due: {task['due_date'] or 'Not set'}"
            for task in tasks
        ]
    )


def mark_task_completed(task_id):
    """Task complete mark karta hai."""
    if db_complete_task(task_id):
        return f"Task {task_id} marked as completed."

    return f"Task {task_id} was not found."


def remove_task(task_id):
    """Task delete karta hai."""
    if db_delete_task(task_id):
        return f"Task {task_id} deleted successfully."

    return f"Task {task_id} was not found."


def task_summary():
    """Task statistics return karta hai."""
    summary = get_task_summary()

    return (
        f"Total Tasks: {summary['total']}\n"
        f"Pending Tasks: {summary['pending']}\n"
        f"Completed Tasks: {summary['completed']}"
    )
