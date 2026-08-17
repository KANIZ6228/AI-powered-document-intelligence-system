import faiss
import numpy as np
import json
import os


class VectorStore:
    """
    FAISS-based vector store for document chunks.
    """

    def __init__(self, dimension: int):
        """
        Create a FAISS index.

        dimension:
            Number of values in each embedding vector.
            all-MiniLM-L6-v2 produces 384-dimensional vectors.
        """

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(dimension)

        self.chunks = []

    def add_embeddings(
        self,
        embeddings,
        chunks
    ):
        """
        Add embeddings and their corresponding
        chunk metadata to the FAISS index.
        """

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding,
        top_k=5
    ):
        """
        Search for the most relevant document chunks.
        """

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # FAISS expects a 2D array
        query_embedding = query_embedding.reshape(
            1,
            -1
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            # FAISS can return -1 if there aren't
            # enough results.
            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append({
                "chunk_id": chunk["chunk_id"],
                "page": chunk["page"],
                "text": chunk["text"],
                "distance": float(distance)
            })

        return results

    def save(self, directory="data/vector_store"):
        """
        Save the FAISS index and chunk metadata.
        """

        os.makedirs(
            directory,
            exist_ok=True
        )

        index_path = os.path.join(
            directory,
            "document.index"
        )

        metadata_path = os.path.join(
            directory,
            "chunks.json"
        )

        faiss.write_index(
            self.index,
            index_path
        )

        with open(
            metadata_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.chunks,
                file,
                ensure_ascii=False,
                indent=2
            )

    @classmethod
    def load(
        cls,
        directory="data/vector_store"
    ):
        """
        Load an existing FAISS index and metadata.
        """

        index_path = os.path.join(
            directory,
            "document.index"
        )

        metadata_path = os.path.join(
            directory,
            "chunks.json"
        )

        index = faiss.read_index(
            index_path
        )

        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            chunks = json.load(file)

        vector_store = cls(
            dimension=index.d
        )

        vector_store.index = index

        vector_store.chunks = chunks

        return vector_store