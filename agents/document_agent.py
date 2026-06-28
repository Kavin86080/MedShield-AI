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

        self.current_document = None

    def load_document(
        self,
        pdf_path
    ):

        print(
            f"\nLoading Document: {pdf_path}"
        )

        self.current_document = pdf_path

        self.pipeline.index_pdf(
            pdf_path,
            reset_index=True
        )

    def run(
        self,
        state
    ):

        question = state.question

        print(
            "\nDOCUMENT QUESTION:"
        )

        print(question)

        result = self.pipeline.ask(
            question
        )

        state.answer = result["answer"]

        state.contexts = result["contexts"]

        state.current_agent = self.name

        state.add_history(
            self.name
        )

        return state