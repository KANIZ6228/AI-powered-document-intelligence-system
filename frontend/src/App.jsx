import { useState } from "react";
import "./App.css";


function App() {

  const [file, setFile] = useState(null);

  const [uploading, setUploading] = useState(false);

  const [uploadResult, setUploadResult] = useState(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [sources, setSources] = useState([]);

  const [asking, setAsking] = useState(false);

  const [error, setError] = useState("");


  // =====================================================
  // Handle file selection
  // =====================================================

  const handleFileChange = (event) => {

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);

    setUploadResult(null);

    setAnswer("");

    setSources([]);

    setError("");
  };


  // =====================================================
  // Upload document
  // =====================================================

  const uploadDocument = async () => {

    if (!file) {

      setError("Please select a PDF or TXT file.");

      return;
    }


    setUploading(true);

    setError("");

    setUploadResult(null);


    const formData = new FormData();

    formData.append("file", file);


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "Upload failed."
        );
      }


      setUploadResult(data);

    } catch (error) {

      setError(error.message);

    } finally {

      setUploading(false);
    }
  };


  // =====================================================
  // Ask question
  // =====================================================

  const askQuestion = async () => {

    if (!question.trim()) {

      setError("Please enter a question.");

      return;
    }


    setAsking(true);

    setError("");

    setAnswer("");

    setSources([]);


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: question,
            top_k: 5
          })
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "Question failed."
        );
      }


      setAnswer(data.answer);

      setSources(data.sources || []);

    } catch (error) {

      setError(error.message);

    } finally {

      setAsking(false);
    }
  };


  return (

    <div className="app">

      {/* =================================================
          Header
      ================================================= */}

      <header className="header">

        <div>

          <h1>
            AI Document Intelligence
          </h1>

          <p>
            Upload a document and ask questions about it.
          </p>

        </div>

      </header>


      <main className="container">


        {/* =================================================
            Upload Section
        ================================================= */}

        <section className="card">

          <h2>
            📄 Upload Document
          </h2>

          <p className="description">
            Upload a PDF or TXT document to begin.
          </p>


          <div className="upload-area">

            <input
              type="file"
              accept=".pdf,.txt"
              onChange={handleFileChange}
            />


            {file && (

              <div className="selected-file">

                <span>
                  📄 {file.name}
                </span>

              </div>

            )}

          </div>


          <button
            className="primary-button"
            onClick={uploadDocument}
            disabled={!file || uploading}
          >

            {uploading
              ? "Processing..."
              : "Upload & Process"
            }

          </button>


          {/* Upload Result */}

          {uploadResult && (

            <div className="success-box">

              <h3>
                ✓ Document processed successfully
              </h3>

              <p>
                <strong>File:</strong>{" "}
                {uploadResult.filename}
              </p>

              <p>
                <strong>Pages:</strong>{" "}
                {uploadResult.pages}
              </p>

              <p>
                <strong>Chunks:</strong>{" "}
                {uploadResult.chunks}
              </p>

              <p>
                <strong>Embedding dimension:</strong>{" "}
                {uploadResult.embedding_dimension}
              </p>

            </div>

          )}

        </section>


        {/* =================================================
            Question Section
        ================================================= */}

        <section className="card">

          <h2>
            💬 Ask Your Document
          </h2>

          <p className="description">
            Ask a question based on the uploaded document.
          </p>


          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            placeholder="What are the main objectives of this research?"
            rows="4"
          />


          <button
            className="primary-button"
            onClick={askQuestion}
            disabled={asking}
          >

            {asking
              ? "Thinking..."
              : "Ask Question"
            }

          </button>

        </section>


        {/* =================================================
            Error
        ================================================= */}

        {error && (

          <div className="error-box">

            ⚠️ {error}

          </div>

        )}


        {/* =================================================
            Answer
        ================================================= */}

        {answer && (

          <section className="card">

            <h2>
              🤖 Answer
            </h2>

            <div className="answer">

              {answer}

            </div>

          </section>

        )}


        {/* =================================================
            Sources
        ================================================= */}

        {sources.length > 0 && (

          <section className="card">

            <h2>
              📚 Sources
            </h2>


            <div className="sources">

              {sources.map(
                (source, index) => (

                  <div
                    className="source"
                    key={index}
                  >

                    <div className="source-header">

                      <strong>
                        Page {source.page}
                      </strong>

                      <span>
                        Chunk {source.chunk_id}
                      </span>

                    </div>


                    <p>
                      {source.excerpt}
                    </p>


                    <small>
                      Relevance score:{" "}
                      {source.relevance_score}
                    </small>

                  </div>

                )
              )}

            </div>

          </section>

        )}

      </main>


      {/* =================================================
          Footer
      ================================================= */}

      <footer>

        <p>
          AI-Powered Document Intelligence System
        </p>

        <p>
          FastAPI • FAISS • Ollama • Llama 3.2 • React
        </p>

      </footer>

    </div>

  );
}


export default App;