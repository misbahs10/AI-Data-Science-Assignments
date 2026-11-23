
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.retriever import MemoryRetriever


class MemoryManager:
    """Central manager for short-term and long-term memory."""

    def __init__(
        self,
        max_short_term_messages=10,
        max_retrieved_memories=5,
        min_similarity=0.30
    ):
        self.short_term = ShortTermMemory(
            max_messages=max_short_term_messages
        )

        self.long_term = LongTermMemory()

        self.retriever = MemoryRetriever(
            top_k=max_retrieved_memories,
            min_similarity=min_similarity
        )

    # ---------------- SHORT-TERM MEMORY ----------------

    def add_message(self, conversation_id, role, content):
        return self.short_term.add_message(
            conversation_id,
            role,
            content
        )

    def get_conversation_context(self, conversation_id):
        return self.short_term.get_context(conversation_id)

    def clear_conversation_context(self, conversation_id):
        return self.short_term.clear_context(conversation_id)

    # ---------------- LONG-TERM MEMORY ----------------

    def save_memory(self, memory, category="general"):
        """Save a memory and immediately index pending memories."""

        memory_id = self.long_term.add_memory(
            memory,
            category
        )

        self.retriever.index_memories()

        return memory_id

    def get_all_memories(self):
        return self.long_term.get_all_memories()

    def search_memories(self, keyword):
        return self.long_term.search_memories(keyword)

    def update_memory(self, memory_id, new_memory, category=None):
        """Update memory and regenerate its embedding."""

        updated = self.long_term.update_existing_memory(
            memory_id,
            new_memory,
            category
        )

        if updated:
            self.retriever.index_memories()

        return updated

    def delete_memory(self, memory_id):
        return self.long_term.delete_existing_memory(memory_id)

    # ---------------- SEMANTIC RETRIEVAL ----------------

    def retrieve_relevant_memories(self, query):
        return self.retriever.retrieve(query)

    # ---------------- COMBINED CONTEXT ----------------

    def get_agent_context(self, conversation_id, query):
        """Return recent conversation and relevant long-term memories."""

        conversation_history = self.get_conversation_context(
            conversation_id
        )

        relevant_memories = self.retrieve_relevant_memories(
            query
        )

        return {
            "conversation_history": conversation_history,
            "relevant_memories": relevant_memories
        }
