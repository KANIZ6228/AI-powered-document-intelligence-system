import ollama


def build_context(results):
    """
    Convert retrieved chunks into a context string
    for the LLM.
    """

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
Page {result['page']}
Chunk {result['chunk_id']}

{result['text']}
"""
        )

    return "\n".join(context_parts)


class LLMService:
    """
    Handles communication with the local Ollama LLM.
    """

    def __init__(
        self,
        model_name: str = "llama3.2:3b"
    ):
        self.model_name = model_name

    def generate_answer(
        self,
        question: str,
        context: str
    ):
        """
        Generate an answer using the retrieved
        document context.
        """

        prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the answer cannot be found in the context,
say:

"I could not find this information in the document."

Do not use outside knowledge.
Do not invent facts.
Do not make unsupported assumptions.

Document Context:
-----------------
{context}
-----------------

User Question:
{question}

Answer:
"""

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]