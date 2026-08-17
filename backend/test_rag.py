from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import EmbeddingModel
from services.vector_store import VectorStore
from services.retriever import Retriever
from services.llm_service import LLMService, build_context


# =========================================
# 1. Load document
# =========================================

file_path = "data/uploads/test.txt"

pages = extract_document(
    file_path
)


# =========================================
# 2. Create chunks
# =========================================

chunks = create_chunks(
    pages,
    chunk_size=300,
    chunk_overlap=50
)


print(
    f"Created {len(chunks)} chunks."
)


# =========================================
# 3. Create embeddings
# =========================================

embedding_model = EmbeddingModel()

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = embedding_model.embed_documents(
    texts
)


# =========================================
# 4. Create FAISS vector store
# =========================================

dimension = embeddings.shape[1]

vector_store = VectorStore(
    dimension=dimension
)

vector_store.add_embeddings(
    embeddings,
    chunks
)


# =========================================
# 5. Create retriever
# =========================================

retriever = Retriever(
    vector_store=vector_store,
    embedding_model=embedding_model
)


# =========================================
# 6. Ask question
# =========================================

question = (
    "What is the main objective "
    "of this research?"
)


# =========================================
# 7. Retrieve relevant chunks
# =========================================

results = retriever.retrieve(
    question=question,
    top_k=3
)


# =========================================
# 8. Build context
# =========================================

context = build_context(
    results
)


print("\n===== RETRIEVED CONTEXT =====\n")

print(context)


# =========================================
# 9. Generate answer
# =========================================

llm = LLMService(
    model_name="llama3.2:3b"
)


answer = llm.generate_answer(
    question=question,
    context=context
)


# =========================================
# 10. Display answer
# =========================================

print("\n===== AI ANSWER =====\n")

print(answer)


# =========================================
# 11. Display sources
# =========================================

print("\n===== SOURCES =====\n")

for result in results:

    print(
        f"Page {result['page']}"
    )

    print(
        result["text"]
    )

    print()