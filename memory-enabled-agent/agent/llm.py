
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from agent.prompts import SYSTEM_PROMPT, build_context_prompt


class GroqLLM:
    """Groq LLM client for Memory AI."""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. Check your .env file."
            )

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = GROQ_MODEL

    def generate_response(
        self,
        user_message,
        conversation_history=None,
        relevant_memories=None
    ):
        """Generate a context-aware AI response."""

        conversation_history = conversation_history or []
        relevant_memories = relevant_memories or []

        memory_context = build_context_prompt(
            conversation_history,
            relevant_memories
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + "\n\n" + memory_context
            }
        ]

        # Add recent conversation history.
        messages.extend(conversation_history)

        # Add the current user message.
        messages.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content
