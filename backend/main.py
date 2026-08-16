from fastapi import FastAPI


app = FastAPI(
    title="AI-Powered Document Intelligence System",
    description="A RAG-based document question answering system.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI-Powered Document Intelligence API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }