
from agent.llm import GroqLLM

llm = GroqLLM()

response = llm.generate_response(
    user_message="What do you know about me?",
    conversation_history=[
        {
            "role": "user",
            "content": "I am learning Python."
        },
        {
            "role": "assistant",
            "content": "That's great! Python is useful for AI development."
        }
    ],
    relevant_memories=[
        {
            "memory": "I am studying Artificial Intelligence and Data Science.",
            "category": "education",
            "similarity": 0.85
        },
        {
            "memory": "I know Python, SQL and Machine Learning.",
            "category": "skills",
            "similarity": 0.80
        }
    ]
)

print("\n--- GROQ AI RESPONSE ---")
print(response)
