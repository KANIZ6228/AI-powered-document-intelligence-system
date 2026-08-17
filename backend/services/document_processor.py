import fitz
import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text.

    Removes unnecessary whitespace while preserving
    the actual content of the document.
    """

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_path: str):
    """
    Extract text from a PDF while preserving page numbers.

    Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
    """

    document = fitz.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text()

        cleaned_text = clean_text(text)

        if cleaned_text:
            pages.append({
                "page": page_number,
                "text": cleaned_text
            })

    document.close()

    return pages


def extract_text_from_txt(file_path: str):
    """
    Extract text from a TXT file.

    TXT files do not have pages, so the entire
    document is treated as page 1.
    """

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        text = file.read()

    cleaned_text = clean_text(text)

    return [
        {
            "page": 1,
            "text": cleaned_text
        }
    ]


def extract_document(file_path: str):
    """
    Detect the document type and extract its text.
    """

    file_path = file_path.lower()

    if file_path.endswith(".pdf"):

        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".txt"):

        return extract_text_from_txt(file_path)

    else:

        raise ValueError(
            "Unsupported file type. "
            "Only PDF and TXT files are supported."
        )