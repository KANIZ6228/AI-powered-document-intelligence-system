from services.document_processor import extract_document


file_path = "data/uploads/demo_organized.pdf"

pages = extract_document(file_path)

print("\n===== EXTRACTED DOCUMENT =====\n")

print(f"Number of pages: {len(pages)}")

for page in pages:

    print(f"\n--- Page {page['page']} ---")
    print(page["text"][:1000])