from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)

from ai_engine.gemini_engine.gemini_service import (
    GeminiService
)


class PDFRAGGeminiPipeline:

    def __init__(self):

        self.pdf_rag = PDFRAGPipeline()

        self.gemini_service = GeminiService()

    def index_pdf(
        self,
        pdf_path
    ):

        return self.pdf_rag.index_pdf(
            pdf_path
        )

    def ask(
        self,
        question,
        top_k=3
    ):

        contexts = (
            self.pdf_rag.query(
                question,
                top_k
            )
        )

        context_text = "\n\n".join(
            contexts
        )

        prompt = f"""
You are MedShield-X.

Use ONLY the retrieved context.

Retrieved Context:
{context_text}

Question:
{question}

Answer:
"""

        answer = (
            self.gemini_service.ask(
                prompt
            )
        )

        return {
            "question": question,
            "answer": answer,
            "contexts": contexts
        }