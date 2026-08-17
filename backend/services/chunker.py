from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(
    pages,
    chunk_size=800,
    chunk_overlap=150
):
    """
    Split extracted document pages into smaller chunks.

    Each chunk keeps:
    - chunk_id
    - page number
    - chunk text
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    chunk_id = 0

    for page in pages:

        page_text = page["text"]

        page_chunks = text_splitter.split_text(
            page_text
        )

        for chunk_text in page_chunks:

            chunks.append({
                "chunk_id": chunk_id,
                "page": page["page"],
                "text": chunk_text
            })

            chunk_id += 1

    return chunks