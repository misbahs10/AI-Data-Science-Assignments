
from memory.long_term import LongTermMemory
from memory.retriever import MemoryRetriever


memory_manager = LongTermMemory()
retriever = MemoryRetriever(top_k=5)

test_memories = [
    ("I am studying Artificial Intelligence and Data Science.", "education"),
    ("I know Python, SQL, Pandas and Machine Learning.", "skills"),
    ("I prefer explanations in Roman Urdu.", "preferences"),
    ("I enjoy building AI agents and automation workflows.", "interests"),
]

saved_ids = []

try:
    print("\n--- SAVING TEST MEMORIES ---")

    for memory, category in test_memories:
        memory_id = memory_manager.add_memory(memory, category)
        saved_ids.append(memory_id)

    print("Test memories saved!")

    print("\n--- INDEXING MEMORIES ---")

    indexed = retriever.index_memories()
    print(f"New memories indexed: {indexed}")

    print("\n--- SEMANTIC SEARCH ---")

    queries = [
        "What am I studying?",
        "Which programming technologies do I know?",
        "How do I prefer explanations?"
    ]

    for query in queries:
        print(f"\nQuery: {query}")

        results = retriever.retrieve(query)

        if not results:
            print("No relevant memories found.")

        for result in results:
            print(
                f"Memory: {result['memory']}\n"
                f"Category: {result['category']}\n"
                f"Similarity: {result['similarity']}"
            )

finally:
    print("\n--- CLEANUP ---")

    for memory_id in set(saved_ids):
        memory_manager.delete_existing_memory(memory_id)

    print("Test memories deleted!")
