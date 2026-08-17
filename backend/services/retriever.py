class Retriever:

    def __init__(
        self,
        vector_store,
        embedding_model
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
        distance_threshold: float = 1.5
    ):
        """
        Retrieve the most relevant document chunks
        for a given question.
        """

        # Create embedding for the user's question
        query_embedding = self.embedding_model.embed_query(
            question
        )

        # Search FAISS
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        # Keep only sufficiently relevant chunks
        filtered_results = [
            result
            for result in results
            if result["distance"] <= distance_threshold
        ]

        return filtered_results