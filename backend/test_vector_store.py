from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import EmbeddingModel
from services.vector_store import VectorStore


# -----------------------------------------
# 1. Load document
# -----------------------------------------

file_path = "data/uploads/test.txt"

pages = extract_document(file_path)


# -----------------------------------------
# 2. Create chunks
# -----------------------------------------

chunks = create_chunks(
    pages,
    chunk_size=300,
    chunk_overlap=50
)


print(
    f"Created {len(chunks)} chunks."
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


print(
    f"Embedding shape: {embeddings.shape}"
)


# -----------------------------------------
# 4. Create vector store
# -----------------------------------------

dimension = embeddings.shape[1]

vector_store = VectorStore(
    dimension=dimension
)


# -----------------------------------------
# 5. Add embeddings
# -----------------------------------------

vector_store.add_embeddings(
    embeddings,
    chunks
)


print(
    f"Vectors stored: {vector_store.index.ntotal}"
)


# -----------------------------------------
# 6. Create question
# -----------------------------------------

question = (
    "What is the main objective "
    "of this research?"
)


# -----------------------------------------
# 7. Embed question
# -----------------------------------------

query_embedding = embedding_model.embed_query(
    question
)


# -----------------------------------------
# 8. Search FAISS
# -----------------------------------------

results = vector_store.search(
    query_embedding,
    top_k=3
)


# -----------------------------------------
# 9. Display results
# -----------------------------------------

print("\n===== SEARCH RESULTS =====\n")


for result in results:

    print("----------------------------")

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

    print(result["text"])
    # -----------------------------------------
# 10. Save vector store
# -----------------------------------------

vector_store.save()

print(
    "\nVector store saved successfully."
)