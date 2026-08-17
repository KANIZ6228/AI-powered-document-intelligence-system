from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Handles text embedding generation using
    a Sentence Transformer model.
    """

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str):
        """
        Convert a single text into an embedding vector.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding

    def embed_documents(self, texts: list[str]):
        """
        Convert multiple text chunks into embeddings.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings

    def embed_query(self, query: str):
        """
        Convert a user question into an embedding vector.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding