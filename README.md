# 🤖 AI-Powered Document Intelligence System

> **Turn lengthy documents into an interactive AI knowledge base.**

A full-stack **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF/TXT documents, process and index their content, and ask natural-language questions with **context-grounded answers and source attribution**.

### 🔄 How it works

**Upload → Extract → Chunk → Embed → Retrieve → Generate → Cite**

<p align="center">

**📄 Document** → **🧠 Embeddings** → **🔎 FAISS Retrieval** → **🤖 Llama 3.2** → **💬 Answer + Sources**

</p>

---

## 🚀 Demo

### 🖥️ Application Preview


### 🎥 Demo Video

> Add your demo video link here after recording it.

**[▶️ Watch the Full Demo](YOUR_VIDEO_LINK_HERE)**


# ⭐ Key Highlights

| Feature                 | Description                                                      |
| ----------------------- | ---------------------------------------------------------------- |
| 📄 Document Processing  | Extracts text from PDF and TXT files                             |
| ✂️ Intelligent Chunking | Splits documents into manageable contextual chunks               |
| 🧠 Semantic Embeddings  | Converts document chunks and queries into vector representations |
| 🔎 Semantic Retrieval   | Retrieves the most relevant document sections using FAISS        |
| 🤖 Local LLM            | Generates answers using Llama 3.2 through Ollama                 |
| 📚 RAG                  | Grounds responses using retrieved document context               |
| 🔍 Source Attribution   | Displays page numbers, chunk IDs and source excerpts             |
| 💾 Persistent Storage   | Saves FAISS index and metadata locally                           |
| ⚡ REST API              | FastAPI backend exposes document and Q&A endpoints               |
| 🖥️ Interactive UI      | React + Vite frontend for document interaction                   |

---

# 💡 Problem

Searching through lengthy documents manually can be time-consuming.

Traditional keyword-based search can also struggle when a user asks a question using different terminology from the original document.

For example:

> **"What methodology did the researchers use?"**

The document may never contain the exact phrase *"what methodology did they use"*.

This project addresses that problem using **semantic retrieval + Retrieval-Augmented Generation (RAG)**.

---

# 🎯 Solution

The system transforms uploaded documents into a searchable knowledge base.

Instead of asking an LLM to answer from its general knowledge, the system:

1. Extracts document content
2. Splits the content into chunks
3. Generates vector embeddings
4. Stores embeddings in FAISS
5. Converts the user's question into an embedding
6. Retrieves the most relevant document chunks
7. Sends the retrieved context to the LLM
8. Generates a grounded answer
9. Returns the supporting source information

This helps reduce unsupported responses and makes answers easier to verify.

---

# 🖥️ Screenshots

## 1. Document Intelligence Dashboard

![Dashboard](screenshots/01-dashboard.png)

The main interface allows users to upload documents and interact with the document knowledge base.

---

## 2. Document Upload & Processing

![Document Upload](screenshots/02-document-upload.png)

Users can upload supported PDF or TXT documents for processing.

The backend performs:

```text
Upload
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
FAISS Indexing
```

---

## 3. AI Question Answering

![Question Answering](screenshots/03-question-answer.png)

Users can ask natural-language questions about the uploaded document.

Example:

> **What are the main objectives of this research?**

The system retrieves relevant document context before generating the response.

---

## 4. Source Attribution

![Source Attribution](screenshots/04-source-attribution.png)

Each answer can be traced back to the retrieved document content.

Example:

```text
📄 research_paper.pdf
Page: 4
Chunk: 7

"The proposed methodology..."
```

This improves transparency and allows users to verify generated answers.

---

## 5. Backend API

![API Documentation](screenshots/05-api-docs.png)

The backend provides interactive API documentation through FastAPI Swagger UI.

Available at:

`http://localhost:8000/docs`

---

# 🎥 Demo Workflow

The application follows this workflow:

```text
                 ┌──────────────────┐
                 │      User        │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Upload Document  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Text Extraction │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Chunking     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    Embeddings    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   FAISS Index    │
                 └────────┬─────────┘
                          │
                          │
                    User Question
                          │
                          ▼
                 ┌──────────────────┐
                 │ Query Embedding  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Semantic Search  │
                 │   Top-K Chunks   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │      Ollama      │
                 │    Llama 3.2     │
                 └────────┬─────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Answer + Source Context│
              └────────────────────────┘
```

---

# 🏗️ System Architecture

The application follows a two-tier full-stack architecture.

```text
┌─────────────────────────────────────────────┐
│                 React Frontend              │
│                 React 19 + Vite              │
└──────────────────────┬──────────────────────┘
                       │ HTTP / CORS
                       ▼
┌─────────────────────────────────────────────┐
│                 FastAPI Backend              │
├─────────────────────────────────────────────┤
│                                             │
│  Document Processing      Question Answering│
│          │                       │           │
│          ▼                       ▼           │
│      Extraction            Query Embedding  │
│          │                       │           │
│          ▼                       ▼           │
│       Chunking             FAISS Search      │
│          │                       │           │
│          ▼                       ▼           │
│      Embeddings             Top-K Chunks     │
│          │                       │           │
│          └───────────┬───────────┘           │
│                      ▼                       │
│                 Ollama / Llama 3.2          │
│                      │                       │
│                      ▼                       │
│               Answer + Sources              │
└─────────────────────────────────────────────┘
```

---

# 🔄 RAG Pipeline

## 1️⃣ Document Ingestion

Supported files:

* PDF
* TXT

PDF text is extracted using **PyMuPDF (fitz)** while preserving page information.

---

## 2️⃣ Text Cleaning

Extracted content is normalized using whitespace and formatting cleanup while preserving useful document structure.

---

## 3️⃣ Text Chunking

Documents are divided using LangChain's `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk Size: 800 characters
Overlap: 150 characters
```

The overlap helps preserve contextual continuity between adjacent chunks.

Each chunk stores metadata such as:

```text
chunk_id
page_number
document_name
text
```

---

## 4️⃣ Embedding Generation

The project uses:

**Sentence Transformers — `all-MiniLM-L6-v2`**

Characteristics:

* 384-dimensional embeddings
* Lightweight
* CPU-friendly
* Suitable for semantic similarity search
* Approximately 80MB model size

---

## 5️⃣ Vector Storage

Embeddings are stored using:

**FAISS — IndexFlatL2**

The index is persisted locally:

```text
data/vector_store/
├── document.index
└── chunks.json
```

This allows the vector store to survive application restarts.

---

## 6️⃣ Retrieval

When the user asks a question:

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Top-5 Relevant Chunks
      ↓
Context Construction
```

The retrieved chunks contain page and chunk metadata for traceability.

---

## 7️⃣ Generation

The retrieved context and user question are passed to:

**Ollama → Llama 3.2:3b**

The model is instructed to answer using the retrieved document context and avoid answering when sufficient evidence is unavailable.

### 🛡️ Hallucination Mitigation

The system does not guarantee zero hallucinations.

Instead, it uses:

* Retrieved document context
* Grounded prompting
* Source attribution
* Out-of-context response handling

to reduce unsupported answers.

---

# 🛠️ Tech Stack

## Backend

| Technology            | Purpose                      |
| --------------------- | ---------------------------- |
| Python                | Core backend and AI pipeline |
| FastAPI               | REST API                     |
| PyMuPDF               | PDF text extraction          |
| LangChain             | Text splitting               |
| Sentence Transformers | Embeddings                   |
| FAISS                 | Vector similarity search     |
| Ollama                | Local LLM inference          |
| Llama 3.2:3b          | Answer generation            |
| Pytest                | Testing                      |

## Frontend

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| React 19   | User interface                  |
| Vite       | Frontend development/build tool |
| CSS        | UI styling                      |

---

# 🧠 Engineering Highlights

### 🔍 Semantic Retrieval

The system uses vector embeddings instead of relying solely on keyword matching.

### 📚 Retrieval-Augmented Generation

LLM responses are generated using retrieved document context.

### 🔎 Source Attribution

Answers can be traced to specific document pages and chunks.

### 💾 Persistent Vector Store

FAISS indexes and metadata are stored locally and reloaded when the application starts.

### 🤖 Local LLM Inference

Ollama enables local model execution without requiring external LLM API calls.

### ⚡ REST API Architecture

The React frontend communicates with the FastAPI backend through HTTP endpoints.

### 🧩 Modular Backend

Document processing, chunking, embeddings, retrieval, vector storage and LLM communication are separated into dedicated services.

---

# 🧪 Evaluation

The project can be evaluated using a set of questions with known answers and source pages.

Example evaluation structure:

```text
Evaluation Dataset
        ↓
Test Questions
        ↓
RAG Pipeline
        ↓
Compare Results
        ↓
Retrieval + Answer Quality
```

### Evaluation Metrics

Potential metrics include:

* Retrieval@K
* Context relevance
* Answer relevance
* Faithfulness
* Response latency

> Add measured evaluation results here once the evaluation dataset has been implemented.

---

# 🧩 Challenges Solved

### Challenge 1 — Preserving document context

**Solution:** Used overlapping recursive chunks and metadata such as page numbers and chunk IDs.

### Challenge 2 — Finding relevant content

**Solution:** Converted document chunks and user queries into embeddings and used FAISS similarity search.

### Challenge 3 — Making answers traceable

**Solution:** Preserved document metadata throughout the retrieval pipeline.

### Challenge 4 — Running an LLM locally

**Solution:** Integrated Ollama with Llama 3.2:3b for local inference.

### Challenge 5 — Separating application layers

**Solution:** Built a React frontend and FastAPI backend communicating through REST APIs.

---

# 📁 Project Structure

```text
AI-powered document intelligence system/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── data/
│   │   ├── uploads/
│   │   └── vector_store/
│   │       ├── chunks.json
│   │       └── document.index
│   │
│   └── services/
│       ├── document_processor.py
│       ├── chunker.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       └── llm_service.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   │
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── main.jsx
│
├── screenshots/
│   ├── 01-dashboard.png
│   ├── 02-document-upload.png
│   ├── 03-question-answer.png
│   ├── 04-source-attribution.png
│   └── 05-api-docs.png
│
├── demo/
│   └── demo.gif
│
├── .gitignore
├── README.md
└── LICENSE
```

---

# 🔌 API Endpoints

## `POST /upload-document`

Uploads and processes a PDF/TXT document.

### Response

```json
{
  "message": "Document processed successfully",
  "chunks_count": 8,
  "page_count": 3
}
```

---

## `POST /ask-question`

Ask a question about the indexed document.

### Request

```json
{
  "question": "What are the main objectives?"
}
```

### Response

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

---

## `POST /reset`

Clears the vector store.

### Response

```json
{
  "message": "Vector store cleared successfully"
}
```

---

# ⚙️ Installation & Setup

## Prerequisites

* Python 3.9+
* Node.js 18+
* npm
* Ollama

Install Ollama and download the required model:

```bash
ollama pull llama3.2:3b
```

---

## 1. Clone Repository

```bash
git clone <repository-url>

cd "AI-powered document intelligence system"
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Start Ollama

```bash
ollama serve
```

Verify the model:

```bash
ollama list
```

---

## 4. Start FastAPI

Inside the `backend` directory:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## 5. Start Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🖥️ Usage

### Step 1 — Upload

Upload a PDF or TXT document.

### Step 2 — Processing

The backend extracts, cleans, chunks and embeds the document.

### Step 3 — Indexing

Embeddings are stored in FAISS.

### Step 4 — Ask

Enter a natural-language question.

### Step 5 — Retrieve

The system retrieves the most relevant document chunks.

### Step 6 — Generate

Llama 3.2 generates an answer using the retrieved context.

### Step 7 — Verify

Review the source document, page number and retrieved excerpt.

---

# 🧪 Testing

Run backend tests:

```bash
cd backend
pytest
```

Build the frontend:

```bash
cd frontend
npm run build
```

Production files are generated in:

```text
frontend/dist/
```

---

# ⚠️ Current Limitations

* Supports PDF and TXT documents
* Primarily optimized for text-based PDFs
* Scanned/image-based PDFs require OCR
* FAISS is currently designed for local/single-application usage
* Local LLM inference depends on available system resources
* Retrieval quality depends on chunking and embedding configuration
* Currently processes one document at a time
* Tables and complex document layouts may not be fully preserved

---

# 🚀 Future Roadmap

## Phase 1 — Retrieval Improvements

* [ ] Hybrid semantic + keyword search
* [ ] Reranking
* [ ] Query rewriting
* [ ] Better chunking strategies

## Phase 2 — Advanced Document Intelligence

* [ ] OCR for scanned PDFs
* [ ] Table extraction
* [ ] Image understanding
* [ ] Multi-document comparison
* [ ] Cross-document reasoning

## Phase 3 — Production Features

* [ ] Docker / Docker Compose
* [ ] Authentication
* [ ] User-specific document collections
* [ ] Cloud deployment
* [ ] Streaming responses
* [ ] Logging and monitoring

## Phase 4 — AI Evaluation

* [ ] Automated RAG evaluation
* [ ] Retrieval benchmarks
* [ ] Faithfulness evaluation
* [ ] Answer relevance evaluation
* [ ] Latency monitoring

---

# 🔐 Environment Variables

Currently the application can use local defaults.

Optional configuration:

```env
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=llama3.2:3b
VITE_API_URL=http://localhost:8000
```

> Never commit API keys, secrets or private configuration files to GitHub.

---

# 🛠️ Design Decisions

## Why FAISS?

* Fast vector similarity search
* Lightweight
* Easy local deployment
* Minimal infrastructure requirements
* Suitable for document-scale datasets

## Why Sentence Transformers?

* Lightweight embedding model
* CPU-friendly
* Strong semantic similarity performance
* No model fine-tuning required

## Why Ollama?

* Local inference
* No external API dependency
* No per-token API cost
* Better privacy for sensitive documents
* Easy model replacement

## Why FastAPI?

* High-performance Python API framework
* Automatic OpenAPI documentation
* Type validation
* Clean REST architecture
* Easy integration with React

## Why React + Vite?

* Component-based frontend
* Fast development workflow
* Lightweight build tooling
* Clear separation between frontend and backend

---

# 🧠 What I Learned

Building this project provided practical experience with:

* Retrieval-Augmented Generation
* Document preprocessing
* Semantic embeddings
* Vector similarity search
* FAISS
* Local LLM inference
* Prompt grounding
* Source attribution
* REST API development
* React frontend development
* Backend/frontend integration
* Error handling
* AI application architecture

---

# 🎯 Project Goals

This project was built to explore how modern AI systems can combine:

```text
Traditional Software Engineering
             +
Document Processing
             +
Semantic Search
             +
Vector Databases
             +
Large Language Models
             ↓
      Intelligent Applications
```

The goal was not simply to build a chatbot, but to understand and implement the complete pipeline behind a practical **RAG-powered AI application**.

---

# 📜 License

This project is created for educational and portfolio purposes.

---

## 👩‍💻 Author

**Kaniz Fatema**

Interested in:

`AI Engineering` • `Machine Learning` • `Data Analytics` • `Full-Stack Development`

---

⭐ If you found this project interesting, consider giving the repository a star!
