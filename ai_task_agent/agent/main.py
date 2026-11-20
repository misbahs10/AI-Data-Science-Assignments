
import os
import sys
import json

from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Project root ko Python path mein add karna
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Environment variables load karna
load_dotenv(PROJECT_ROOT / ".env")

# Task management tools
from tools.task_tool import (
    create_task,
    list_tasks,
    mark_task_completed,
    remove_task,
    task_summary
)

from tools.calculator_tool import calculate


# Groq API configuration
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY missing hai. Project root mein .env check karo."
    )

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


# AI Agent ke available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task in the task manager.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "due_date": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["Low", "Medium", "High"]
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Show all tasks or filter by task status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": ["string", "null"],
                        "enum": ["Pending", "Completed", None]
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_completed",
            "description": "Mark a task as completed using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Delete a task using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "task_summary",
            "description": "Get total, pending and completed task statistics.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]


# Python functions ko tool names ke saath map karna
available_functions = {
    "create_task": create_task,
    "list_tasks": list_tasks,
    "mark_task_completed": mark_task_completed,
    "remove_task": remove_task,
    "task_summary": task_summary,
    "calculate": calculate
}


SYSTEM_PROMPT = """
You are an intelligent AI Task Manager Assistant.

Your responsibilities:
1. Create tasks when users request them.
2. Show tasks when users ask to view their tasks.
3. Complete tasks using their actual task IDs.
4. Delete tasks using their actual task IDs.
5. Provide task statistics and summaries.
6. Perform mathematical calculations when requested.

Important rules:
- Always use the appropriate tool for task operations.
- Never claim a task was created, completed or deleted without
  a successful tool result.
- Never invent task IDs.
- If the user does not specify a task ID for completion or deletion,
  first list the tasks and ask which one they mean.
- Use High, Medium or Low priority.
- Respond clearly and concisely.
"""


def run_agent(user_message: str) -> str:
    """User message process karke AI agent ka response return karta hai."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    # Maximum iterations to avoid infinite tool-calling loops
    for _ in range(8):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            return message.content or "I could not generate a response."

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            try:
                function_args = json.loads(
                    tool_call.function.arguments
                )

                if function_name not in available_functions:
                    result = "Error: Unknown tool requested."
                else:
                    result = available_functions[function_name](
                        **function_args
                    )

            except Exception as error:
                result = f"Tool execution failed: {error}"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "Agent stopped after reaching the maximum tool-call limit."


if __name__ == "__main__":

    print("\n===== AI TASK MANAGER AGENT =====")
    print("Type 'exit' to stop.\n")

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        if not user_input:
            continue

        try:
            answer = run_agent(user_input)
            print(f"\nAgent: {answer}\n")

        except Exception as error:
            print(f"\nAgent Error: {error}\n")
