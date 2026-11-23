
from memory.database import (
    initialize_database,
    create_conversation,
    save_message,
    get_messages,
    get_conversations,
    save_memory,
    get_memories,
    delete_memory
)


# Initialize database
initialize_database()

# Create conversation
conversation_id = create_conversation(
    "My First AI Conversation"
)

# Save messages
save_message(
    conversation_id,
    "user",
    "My name is Misbah."
)

save_message(
    conversation_id,
    "assistant",
    "Nice to meet you, Misbah!"
)

# Save long-term memory
memory_id = save_memory(
    "User is learning Artificial Intelligence and Data Science.",
    "education"
)

# Retrieve conversations
print("\n--- CONVERSATIONS ---")
print(get_conversations())

# Retrieve messages
print("\n--- MESSAGES ---")
print(get_messages(conversation_id))

# Retrieve memories
print("\n--- LONG-TERM MEMORIES ---")
print(get_memories())

# Delete test memory
delete_memory(memory_id)

print("\nDatabase testing completed!")
