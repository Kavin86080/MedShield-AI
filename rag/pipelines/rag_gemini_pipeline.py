from rag.pipelines.rag_pipeline import (
    RAGPipeline
)

from ai_engine.gemini_engine.gemini_service import (
    GeminiService
)


class RAGGeminiPipeline:

    def __init__(self):

        self.rag_pipeline = RAGPipeline()

        self.gemini_service = GeminiService()

    def index_documents(
        self,
        documents
    ):

        self.rag_pipeline.index_documents(
            documents
        )

    def ask(
        self,
        question,
        top_k=3
    ):

        prompt = self.rag_pipeline.build_prompt(
            question=question,
            top_k=top_k
        )

        answer = self.gemini_service.ask(
            prompt
        )

        return {
            "question": question,
            "prompt": prompt,
            "answer": answer
        }