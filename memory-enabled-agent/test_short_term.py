
from memory.database import create_conversation
from memory.short_term import ShortTermMemory


# Initialize memory
memory = ShortTermMemory(max_messages=4)

# Create conversation
conversation_id = create_conversation(
    "Short-Term Memory Test"
)

# Add conversation messages
memory.add_message(
    conversation_id,
    "user",
    "My name is Misbah."
)

memory.add_message(
    conversation_id,
    "assistant",
    "Nice to meet you, Misbah!"
)

memory.add_message(
    conversation_id,
    "user",
    "I am learning Python and AI."
)

memory.add_message(
    conversation_id,
    "assistant",
    "That's great! Python is useful for AI."
)

memory.add_message(
    conversation_id,
    "user",
    "What am I learning?"
)


# Retrieve recent context
print("\n--- SHORT-TERM MEMORY ---")

context = memory.get_context(conversation_id)

for message in context:
    print(f"{message['role']}: {message['content']}")


# Display context count
print("\n--- CONTEXT STATISTICS ---")

print(
    f"Messages in context: "
    f"{memory.get_context_count(conversation_id)}"
)

print(
    f"Maximum messages: {memory.max_messages}"
)

print("\nShort-term memory test completed!")
