
import json
import math

from fastembed import TextEmbedding

from memory.database import get_connection


class MemoryRetriever:
    """Retrieve relevant long-term memories using semantic similarity."""

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5",
        top_k=5,
        min_similarity=0.30
    ):
        self.top_k = top_k
        self.min_similarity = min_similarity

        self.model = TextEmbedding(model_name=model_name)

    def generate_embedding(self, text):
        """Convert text into a numerical vector."""

        embeddings = list(self.model.embed([text]))

        return embeddings[0].tolist()

    @staticmethod
    def cosine_similarity(vector_a, vector_b):
        """Calculate cosine similarity between two vectors."""

        dot_product = sum(
            a * b for a, b in zip(vector_a, vector_b)
        )

        norm_a = math.sqrt(sum(a * a for a in vector_a))
        norm_b = math.sqrt(sum(b * b for b in vector_b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def index_memories(self):
        """Generate embeddings for memories that are not indexed."""

        indexed_count = 0

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, memory
                FROM memories
                WHERE embedding IS NULL
                """
            ).fetchall()

            for row in rows:
                embedding = self.generate_embedding(row["memory"])

                connection.execute(
                    """
                    UPDATE memories
                    SET embedding = ?
                    WHERE id = ?
                    """,
                    (json.dumps(embedding), row["id"])
                )

                indexed_count += 1

        return indexed_count

    def retrieve(self, query):
        """Find memories semantically related to a query."""

        if not query or not query.strip():
            return []

        # Index newly added memories first.
        self.index_memories()

        query_embedding = self.generate_embedding(query.strip())

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, memory, category, embedding
                FROM memories
                WHERE embedding IS NOT NULL
                """
            ).fetchall()

        results = []

        for row in rows:
            stored_embedding = json.loads(row["embedding"])

            similarity = self.cosine_similarity(
                query_embedding,
                stored_embedding
            )

            if similarity >= self.min_similarity:
                results.append({
                    "id": row["id"],
                    "memory": row["memory"],
                    "category": row["category"],
                    "similarity": round(similarity, 4)
                })

        results.sort(
            key=lambda item: item["similarity"],
            reverse=True
        )

        return results[:self.top_k]
