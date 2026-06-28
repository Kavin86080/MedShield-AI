from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)

from ai_engine.groq_engine.groq_service import (
    GroqService
)


class PDFRAGGeminiPipeline:

    def __init__(self):

        self.pdf_rag = (
            PDFRAGPipeline()
        )

        self.groq_service = (
            GroqService()
        )

    def index_pdf(
        self,
        pdf_path,
        reset_index=True
    ):

        return self.pdf_rag.index_pdf(
            pdf_path,
            reset_index=reset_index
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
        print("\n" + "="*50)
        print("QUESTION:")
        print(question)

        print("\nRETRIEVED CONTEXTS:")

        for i, ctx in enumerate(contexts):
            print(f"\nChunk {i+1}:")
            print(ctx[:500])

        print("="*50)
        print("\nRETRIEVED CONTEXTS:")
        print(contexts[:2])

        context_text = "\n\n".join(
            contexts
        )

        prompt = f"""
You are MedShield-X Clinical Document Analysis Assistant.

Use ONLY the provided document context.

Document Context:
{context_text}

Question:
{question}

Instructions:

1. Answer only from the document.
2. Summarize clearly.
3. Use bullet points when appropriate.
4. Mention important findings.
5. Mention conclusions if available.
6. Do not invent information.

Answer:
"""

        answer = (
            self.groq_service.ask(
                prompt
            )
        )

        return {
            "question": question,
            "answer": answer,
            "contexts": contexts
        }