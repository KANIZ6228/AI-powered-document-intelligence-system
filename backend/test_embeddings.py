from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import EmbeddingModel


# ---------------------------------
# 1. Load document
# ---------------------------------

file_path = "data/uploads/test.txt"

pages = extract_document(file_path)


# ---------------------------------
# 2. Create chunks
# ---------------------------------

chunks = create_chunks(
    pages,
    chunk_size=300,
    chunk_overlap=50
)


# ---------------------------------
# 3. Extract chunk text
# ---------------------------------

texts = [
    chunk["text"]
    for chunk in chunks
]


# ---------------------------------
# 4. Create embedding model
# ---------------------------------

embedding_model = EmbeddingModel()


# ---------------------------------
# 5. Generate embeddings
# ---------------------------------

embeddings = embedding_model.embed_documents(
    texts
)


# ---------------------------------
# 6. Display results
# ---------------------------------

print("\n===== EMBEDDING RESULT =====\n")

print(
    "Number of chunks:",
    len(chunks)
)

print(
    "Embedding shape:",
    embeddings.shape
)

print(
    "First embedding:"
)

print(
    embeddings[0]
)
question = "What is the main objective of this research?"

query_embedding = embedding_model.embed_query(
    question
)

print("\n===== QUERY EMBEDDING =====\n")

print(
    "Query embedding shape:",
    query_embedding.shape
)

print(
    query_embedding
)