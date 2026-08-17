# AI-Powered Document Intelligence System

A Retrieval Augmented Generation (RAG) system that allows users to upload PDF/TXT documents, extract and process text, generate embeddings, and ask intelligent questions about document content with source attribution.

## Project Overview

This application implements a complete RAG pipeline with:
- **Document Processing**: Extract text from PDF and TXT files
- **Text Chunking**: Split documents into meaningful semantic chunks
- **Semantic Search**: Use embeddings to find relevant document sections
- **Retrieval Augmented Generation**: Generate answers based on retrieved context
- **Source Attribution**: Display the exact document excerpts used to answer questions

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Text Extraction**: PyMuPDF (fitz)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: FAISS (CPU)
- **LLM**: Ollama with llama3.2:3b model
- **Text Splitting**: LangChain

### Frontend
- **Framework**: React 19 with Vite
- **Styling**: CSS
- **Build Tool**: Vite

## Architecture & Design Decisions

### 1. **Two-Tier Architecture**
- **Backend**: FastAPI REST API for document processing and question answering
- **Frontend**: React SPA for user interactions
- **Communication**: HTTP/CORS for cross-origin requests

### 2. **Document Processing Pipeline**
```
Upload File → Extract Text → Clean Text → Create Chunks → Generate Embeddings → Store in FAISS
```

- **Extraction**: PyMuPDF for robust PDF handling; preserves page numbers
- **Cleaning**: Regex-based whitespace normalization while preserving structure
- **Chunking**: RecursiveCharacterTextSplitter for semantic preservation
  - Chunk size: 800 characters with 150-character overlap
  - Hierarchical separators preserve sentence boundaries
  - Metadata includes chunk_id and page number for attribution

### 3. **Embedding Strategy**
- **Model**: Sentence Transformers (all-MiniLM-L6-v2)
  - 384-dimensional embeddings
  - Lightweight and efficient (~80MB)
  - Excellent semantic understanding
  - Works well without fine-tuning
- **Indexing**: FAISS IndexFlatL2 for fast similarity search

### 4. **Vector Store Persistence**
- FAISS index saved to disk (`data/vector_store/document.index`)
- Chunk metadata persisted as JSON (`data/vector_store/chunks.json`)
- Automatic loading on application startup to preserve indexed documents

### 5. **LLM Integration**
- **Local LLM**: Ollama with llama3.2:3b for privacy and performance
- **Context-Based Generation**: LLM receives retrieved chunks + user question
- **System Prompt**: Ensures answers are grounded in document context
- **No Hallucination**: Model instructed to say "I don't know" for out-of-context questions

### 6. **Retrieval Process**
```
User Question → Embed Question → Search FAISS → Retrieve Top-5 Chunks → Build Context → LLM Response
```

- Top-5 most relevant chunks retrieved by cosine similarity
- Context includes page numbers and chunk IDs for traceability
- Source attribution embedded in response

## Project Structure

```
AI-powered document intelligence system/
├── backend/
│   ├── main.py                          # FastAPI application & routes
│   ├── requirements.txt                 # Python dependencies
│   ├── data/
│   │   ├── uploads/                     # Uploaded documents
│   │   └── vector_store/
│   │       ├── chunks.json              # Chunk metadata
│   │       └── document.index           # FAISS index
│   └── services/
│       ├── document_processor.py        # PDF/TXT extraction
│       ├── chunker.py                   # Text splitting
│       ├── embeddings.py                # Embedding generation
│       ├── vector_store.py              # FAISS operations
│       ├── retriever.py                 # Semantic search
│       └── llm_service.py               # LLM communication
├── frontend/
│   ├── package.json                     # Node dependencies
│   ├── vite.config.js                   # Vite configuration
│   ├── index.html                       # Entry HTML
│   └── src/
│       ├── App.jsx                      # Main React component
│       ├── App.css                      # Styles
│       └── main.jsx                     # React entry point
└── README.md                            # This file
```

## Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **Ollama** installed with `llama3.2:3b` model
  - Download from: https://ollama.ai
  - Pull model: `ollama pull llama3.2:3b`

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "AI-powered document intelligence system"
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Verify Ollama is Running
```bash
ollama serve
# In another terminal, verify the model is available:
ollama list
```

#### Start Backend Server
```bash
uvicorn main:app --reload
```
- API runs at: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm run dev
```
- Frontend runs at: `http://localhost:5173`
- Hot reload enabled for development

## API Endpoints

### `POST /upload-document`
Upload and process a document.

**Request:**
```
Content-Type: multipart/form-data
Body: file (PDF or TXT)
```

**Response:**
```json
{
  "message": "Document processed successfully",
  "chunks_count": 8,
  "page_count": 3
}
```

### `POST /ask-question`
Ask a question about the uploaded document.

**Request:**
```json
{
  "question": "What are the main objectives?"
}
```

**Response:**
```json
{
  "answer": "The research focuses on improving retinal disease classification...",
  "sources": [
    {
      "page": 2,
      "chunk_id": 3,
      "text": "The research focuses on improving retinal disease classification..."
    }
  ]
}
```

### `POST /reset`
Clear the vector store and prepare for a new document.

**Response:**
```json
{
  "message": "Vector store cleared successfully"
}
```

## Usage

1. **Open** `http://localhost:5173` in your browser
2. **Upload** a PDF or TXT file using the file input
3. **Wait** for the document to be processed (extraction, chunking, embedding)
4. **Ask** questions about the document content
5. **View** answers with source attribution showing exact document excerpts

## Key Features

✅ **Document Support**: PDF and TXT files
✅ **Semantic Search**: Find relevant content using embeddings
✅ **Source Attribution**: Know where answers come from
✅ **Page Tracking**: Metadata preserves original page numbers
✅ **Persistent Storage**: Vector store survives application restarts
✅ **CORS Enabled**: Frontend and backend can run on different ports
✅ **Error Handling**: Graceful error messages for unsupported files

## Performance Characteristics

- **Embedding Generation**: ~1-2s for typical documents
- **Question Answering**: ~3-5s (depends on LLM response time)
- **Memory Usage**: ~500MB for all services
- **Vector Search**: <100ms for similarity lookup

## Development & Testing

### Running Tests
```bash
cd backend
pytest
```

### Building Frontend for Production
```bash
cd frontend
npm run build
```

Output files go to `frontend/dist/`

## Design Rationale

### Why FAISS?
- Fast, scalable vector similarity search
- Minimal dependencies
- Persistent index support
- Efficient for document-sized datasets

### Why Sentence Transformers?
- Pre-trained on semantic similarity tasks
- No GPU required
- Lightweight model size
- Works well out-of-the-box

### Why Local LLM (Ollama)?
- Privacy: No API keys or external calls
- Cost-effective: No per-token charges
- Customizable: Can swap models easily
- Fast iteration during development

### Why FastAPI?
- Modern, async-capable
- Automatic API documentation
- Type hints for validation
- CORS middleware built-in

## Future Enhancements (Bonus Features)

1. **Conversation Memory**: Maintain context across multiple questions
2. **Hybrid Search**: Combine semantic and keyword-based search
3. **Evaluation Framework**: Measure retrieval accuracy and hallucination rate
4. **Streaming Responses**: Real-time LLM output to frontend
5. **Docker Deployment**: Complete containerization with docker-compose
6. **Multiple Document Support**: Store and search across multiple documents
7. **Query Optimization**: Automatic prompt engineering

## Troubleshooting

### "Ollama connection refused"
- Ensure Ollama is running: `ollama serve`
- Check if model is installed: `ollama list`

### "CUDA out of memory"
- Using CPU mode is default and sufficient for small documents
- No GPU required for this implementation

### "ModuleNotFoundError"
- Verify virtual environment is activated
- Run `pip install -r requirements.txt` again

### "Port already in use"
- Backend: Change port with `uvicorn main:app --reload --port 8001`
- Frontend: Vite will use next available port automatically

## File Limits

- **Max File Size**: 50MB (configurable in FastAPI)
- **Max Text Length**: Typically 10MB of extracted text per document
- **Recommended**: Documents under 100 pages or 5MB

## Environment Variables

Currently uses defaults. To customize:

```bash
# Backend
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=llama3.2:3b

# Frontend (in .env)
VITE_API_URL=http://localhost:8000
```

## License

This is a demonstration project created for the AI Software Engineer Technical Pre-Assessment.

## Support

For issues or questions, refer to the project requirements and API documentation at `http://localhost:8000/docs`
