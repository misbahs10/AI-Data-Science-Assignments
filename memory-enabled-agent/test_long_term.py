
from memory.long_term import LongTermMemory


# Initialize long-term memory
memory = LongTermMemory()

# 1. Save memories
print("\n--- SAVING MEMORIES ---")

memory_id_1 = memory.add_memory(
    "User is learning Artificial Intelligence and Data Science.",
    "education"
)

memory_id_2 = memory.add_memory(
    "User knows Python, SQL and Machine Learning.",
    "skills"
)

memory_id_3 = memory.add_memory(
    "User prefers explanations in Roman Urdu.",
    "preferences"
)

print("Memories saved successfully!")

# 2. Retrieve all memories
print("\n--- ALL MEMORIES ---")

for item in memory.get_all_memories():
    print(
        f"ID: {item['id']} | "
        f"Category: {item['category']} | "
        f"Memory: {item['memory']}"
    )

# 3. Search memories
print("\n--- SEARCH RESULTS ---")

results = memory.search_memories("Python")

for item in results:
    print(item["memory"])

# 4. Retrieve by category
print("\n--- EDUCATION MEMORIES ---")

education = memory.get_memories_by_category("education")

for item in education:
    print(item["memory"])

# 5. Update memory
print("\n--- UPDATING MEMORY ---")

memory.update_existing_memory(
    memory_id_2,
    "User knows Python, SQL, Machine Learning and FastAPI."
)

print("Memory updated successfully!")

# 6. Count memories
print("\n--- MEMORY STATISTICS ---")

print("Total memories:", memory.get_memory_count())

# 7. Delete test memories
print("\n--- CLEANUP ---")

memory.delete_existing_memory(memory_id_1)
memory.delete_existing_memory(memory_id_2)
memory.delete_existing_memory(memory_id_3)

print("Test memories deleted successfully!")

print("\nLong-term memory testing completed!")
