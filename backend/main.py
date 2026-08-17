from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import EmbeddingModel
from services.vector_store import VectorStore
from services.retriever import Retriever
from services.llm_service import LLMService, build_context


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="AI-Powered Document Intelligence System",
    description="A RAG-based document question answering system",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# Directories
# =========================================================

UPLOAD_DIR = "data/uploads"

VECTOR_STORE_DIR = "data/vector_store"


# Create directories if they don't exist

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    VECTOR_STORE_DIR,
    exist_ok=True
)


# =========================================================
# Global AI Services
# =========================================================

# Embedding model
embedding_model = EmbeddingModel()


# Local LLM through Ollama
llm_service = LLMService(
    model_name="llama3.2:3b"
)


# =========================================================
# Load Existing Vector Store
# =========================================================

def load_existing_vector_store():

    """
    Load an existing FAISS vector store from disk.

    This allows the application to keep the indexed
    document even after restarting FastAPI.
    """

    try:

        index_path = os.path.join(
            VECTOR_STORE_DIR,
            "document.index"
        )

        chunks_path = os.path.join(
            VECTOR_STORE_DIR,
            "chunks.json"
        )

        # Check whether saved vector store exists

        if (
            os.path.exists(index_path)
            and
            os.path.exists(chunks_path)
        ):

            print(
                "Loading existing vector store..."
            )

            store = VectorStore.load(
                VECTOR_STORE_DIR
            )

            print(
                "Vector store loaded successfully."
            )

            return store

    except Exception as e:

        print(
            f"Could not load vector store: {e}"
        )

    return None


# Load vector store when application starts

vector_store = load_existing_vector_store()


# =========================================================
# Current Document
# =========================================================

current_document = None


# =========================================================
# Request Model
# =========================================================

class QuestionRequest(BaseModel):

    question: str

    top_k: int = 5


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {

        "message":
        "AI-Powered Document Intelligence API is running",

        "version": "1.0.0"
    }


# =========================================================
# Document Status Endpoint
# =========================================================

@app.get("/document")
def get_document():

    """
    Return information about the currently indexed document.
    """

    global vector_store
    global current_document


    # No document loaded

    if vector_store is None:

        return {

            "uploaded": False,

            "filename": None,

            "chunks": 0
        }


    # Document exists

    return {

        "uploaded": True,

        "filename": current_document,

        "chunks": vector_store.index.ntotal
    }


# =========================================================
# Upload Document Endpoint
# =========================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global vector_store
    global current_document


    # -----------------------------------------------------
    # 1. Validate File
    # -----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )


    filename = file.filename.lower()


    if not filename.endswith(
        (".pdf", ".txt")
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )


    # -----------------------------------------------------
    # 2. Save Uploaded File
    # -----------------------------------------------------

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )


    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {str(e)}"
        )


    # Store current document name

    current_document = file.filename


    # -----------------------------------------------------
    # 3. Extract Document Text
    # -----------------------------------------------------

    try:

        pages = extract_document(
            file_path
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Document extraction failed: {str(e)}"
        )


    if not pages:

        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from the document."
        )


    # -----------------------------------------------------
    # 4. Create Chunks
    # -----------------------------------------------------

    try:

        chunks = create_chunks(
            pages,
            chunk_size=800,
            chunk_overlap=150
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chunk creation failed: {str(e)}"
        )


    if not chunks:

        raise HTTPException(
            status_code=400,
            detail="Could not create document chunks."
        )


    # -----------------------------------------------------
    # 5. Generate Embeddings
    # -----------------------------------------------------

    try:

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = embedding_model.embed_documents(
            texts
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Embedding generation failed: {str(e)}"
        )


    # -----------------------------------------------------
    # 6. Create FAISS Vector Store
    # -----------------------------------------------------

    try:

        dimension = embeddings.shape[1]

        vector_store = VectorStore(
            dimension=dimension
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Vector store creation failed: {str(e)}"
        )


    # -----------------------------------------------------
    # 7. Add Embeddings to FAISS
    # -----------------------------------------------------

    try:

        vector_store.add_embeddings(
            embeddings,
            chunks
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to store embeddings: {str(e)}"
        )


    # -----------------------------------------------------
    # 8. Save FAISS Vector Store
    # -----------------------------------------------------

    try:

        vector_store.save(
            VECTOR_STORE_DIR
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save vector store: {str(e)}"
        )


    # -----------------------------------------------------
    # 9. Return Upload Information
    # -----------------------------------------------------

    return {

        "message":
        "Document processed successfully.",

        "filename":
        file.filename,

        "pages":
        len(pages),

        "chunks":
        len(chunks),

        "embedding_dimension":
        dimension
    }


# =========================================================
# Ask Question Endpoint
# =========================================================

@app.post("/ask")
async def ask_question(
    request: QuestionRequest
):

    global vector_store


    # -----------------------------------------------------
    # 1. Check Document
    # -----------------------------------------------------

    if vector_store is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a document first."
        )


    # -----------------------------------------------------
    # 2. Validate Question
    # -----------------------------------------------------

    question = request.question.strip()


    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # -----------------------------------------------------
    # 3. Validate top_k
    # -----------------------------------------------------

    if request.top_k < 1:

        raise HTTPException(
            status_code=400,
            detail="top_k must be at least 1."
        )


    # Prevent excessively large searches

    top_k = min(
        request.top_k,
        10
    )


    # -----------------------------------------------------
    # 4. Create Retriever
    # -----------------------------------------------------

    retriever = Retriever(
        vector_store=vector_store,

        embedding_model=embedding_model
    )


    # -----------------------------------------------------
    # 5. Retrieve Relevant Chunks
    # -----------------------------------------------------

    try:

        results = retriever.retrieve(
            question=question,
            top_k=top_k
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Document retrieval failed: {str(e)}"
        )


    # -----------------------------------------------------
    # 6. No Relevant Information
    # -----------------------------------------------------

    if not results:

        return {

            "question": question,

            "answer":
            "I could not find this information in the document.",

            "sources": []
        }


    # -----------------------------------------------------
    # 7. Build Context
    # -----------------------------------------------------

    context = build_context(
        results
    )


    # -----------------------------------------------------
    # 8. Generate LLM Answer
    # -----------------------------------------------------

    try:

        answer = llm_service.generate_answer(
            question=question,

            context=context
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {str(e)}"
        )


    # -----------------------------------------------------
    # 9. Prepare Sources
    # -----------------------------------------------------

    sources = []


    for result in results:

        sources.append({

            "page":
            result["page"],

            "chunk_id":
            result["chunk_id"],

            "excerpt":
            result["text"],

            "relevance_score":
            round(
                result["distance"],
                4
            )
        })


    # -----------------------------------------------------
    # 10. Return Final Response
    # -----------------------------------------------------

    return {

        "question":
        question,

        "answer":
        answer,

        "sources":
        sources
    }