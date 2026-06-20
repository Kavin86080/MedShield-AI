from agents.base_agent import BaseAgent

from rag.pipelines.pdf_rag_gemini_pipeline import (
    PDFRAGGeminiPipeline
)


class DocumentAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="DocumentAgent"
        )

        self.pipeline = (
            PDFRAGGeminiPipeline()
        )

    def load_document(
        self,
        pdf_path
    ):

        self.pipeline.index_pdf(
            pdf_path
        )

    def run(
        self,
        state
    ):

        question = (
            state.question
        )

        result = (
            self.pipeline.ask(
                question
            )
        )

        state.answer = (
            result["answer"]
        )

        state.contexts = (
            result["contexts"]
        )

        state.current_agent = (
            self.name
        )

        state.add_history(
            self.name
        )

        return state