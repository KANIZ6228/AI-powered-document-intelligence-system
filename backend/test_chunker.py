from services.document_processor import extract_document
from services.chunker import create_chunks


file_path = "data/uploads/test.txt"


# Step 1: Extract the document
pages = extract_document(file_path)


# Step 2: Create chunks
chunks = create_chunks(
    pages,
    chunk_size=300,
    chunk_overlap=50
)


print("\n===== CHUNKING RESULT =====\n")

print(f"Number of pages: {len(pages)}")
print(f"Number of chunks: {len(chunks)}")


for chunk in chunks:

    print("\n-----------------------------")

    print(f"Chunk ID: {chunk['chunk_id']}")
    print(f"Page: {chunk['page']}")

    print("\nText:")
    print(chunk["text"])