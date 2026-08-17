from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import EmbeddingModel
from services.vector_store import VectorStore
from services.retriever import Retriever


# -----------------------------------------
# 1. Load document
# -----------------------------------------

file_path = "data/uploads/test.txt"

pages = extract_document(
    file_path
)


# -----------------------------------------
# 2. Create chunks
# -----------------------------------------

chunks = create_chunks(
    pages,
    chunk_size=300,
    chunk_overlap=50
)


# -----------------------------------------
# 3. Create embeddings
# -----------------------------------------

embedding_model = EmbeddingModel()

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = embedding_model.embed_documents(
    texts
)


# -----------------------------------------
# 4. Create vector store
# -----------------------------------------

dimension = embeddings.shape[1]

vector_store = VectorStore(
    dimension=dimension
)


# -----------------------------------------
# 5. Store embeddings
# -----------------------------------------

vector_store.add_embeddings(
    embeddings,
    chunks
)


# -----------------------------------------
# 6. Create retriever
# -----------------------------------------

retriever = Retriever(
    vector_store=vector_store,
    embedding_model=embedding_model
)


# -----------------------------------------
# 7. Ask question
# -----------------------------------------

question = (
    "What is the main objective "
    "of this research?"
)


# -----------------------------------------
# 8. Retrieve relevant chunks
# -----------------------------------------

results = retriever.retrieve(
    question=question,
    top_k=3
)


# -----------------------------------------
# 9. Display results
# -----------------------------------------

print("\n===== RETRIEVAL RESULTS =====\n")

print(
    f"Question: {question}"
)

print(
    f"\nRetrieved {len(results)} chunks:\n"
)


for result in results:

    print("-----------------------------")

    print(
        f"Chunk ID: {result['chunk_id']}"
    )

    print(
        f"Page: {result['page']}"
    )

    print(
        f"Distance: {result['distance']:.4f}"
    )

    print("\nText:")

    print(
        result["text"]
    )