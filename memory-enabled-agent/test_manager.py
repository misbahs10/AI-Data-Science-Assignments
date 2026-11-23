
from memory.database import initialize_database, create_conversation
from memory.manager import MemoryManager


initialize_database()

manager = MemoryManager(
    max_short_term_messages=5,
    max_retrieved_memories=3
)

conversation_id = create_conversation(
    "Memory Manager Test"
)

try:
    print("\n--- SHORT-TERM MEMORY ---")

    manager.add_message(
        conversation_id,
        "user",
        "I am learning Artificial Intelligence."
    )

    manager.add_message(
        conversation_id,
        "assistant",
        "That is great! What technologies are you learning?"
    )

    manager.add_message(
        conversation_id,
        "user",
        "I am learning Python and Machine Learning."
    )

    history = manager.get_conversation_context(conversation_id)

    for message in history:
        print(f"{message['role']}: {message['content']}")

    print("\n--- LONG-TERM MEMORY ---")

    memory_id = manager.save_memory(
        "I enjoy developing AI agents using Python.",
        "interests"
    )

    print(f"Memory saved with ID: {memory_id}")

    print("\n--- SEMANTIC RETRIEVAL ---")

    query = "What do I enjoy developing?"

    results = manager.retrieve_relevant_memories(query)

    for result in results:
        print(
            f"Memory: {result['memory']}\n"
            f"Category: {result['category']}\n"
            f"Similarity: {result['similarity']}\n"
        )

    print("\n--- COMBINED AGENT CONTEXT ---")

    context = manager.get_agent_context(
        conversation_id,
        query
    )

    print("Conversation messages:", len(context["conversation_history"]))
    print("Relevant memories:", len(context["relevant_memories"]))

    print("\nMemory Manager testing completed!")

finally:
    manager.delete_memory(memory_id)

    # Remove only this test conversation and its messages.
    from memory.database import delete_conversation
    delete_conversation(conversation_id)

    print("\nTest data cleaned up.")
