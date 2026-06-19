# Placeholder for rag_pipeline.py
from rag.retrievers.dense_retriever import (
    DenseRetriever
)

from ai_engine.prompt_engine.prompt_engine import (
    PromptEngine
)


class RAGPipeline:

    def __init__(self):

        self.retriever = DenseRetriever()

        self.prompt_engine = PromptEngine()

    def index_documents(
        self,
        documents
    ):
        """
        Index documents into FAISS
        """

        self.retriever.index_documents(
            documents
        )

    def retrieve_context(
        self,
        question,
        top_k=3
    ):
        """
        Retrieve relevant chunks
        """

        return self.retriever.retrieve(
            query=question,
            top_k=top_k
        )

    def build_prompt(
        self,
        question,
        top_k=3
    ):
        """
        Create RAG prompt
        """

        contexts = self.retrieve_context(
            question,
            top_k
        )

        context_text = "\n\n".join(
            contexts
        )

        prompt = self.prompt_engine.build_prompt(
            template_name="rag",
            question=question,
            context=context_text
        )

        return prompt

    def query(
        self,
        question,
        top_k=3
    ):
        """
        Phase-3:
        Returns prompt only.

        Gemini integration comes in Phase-4.
        """

        prompt = self.build_prompt(
            question,
            top_k
        )

        return {
            "question": question,
            "prompt": prompt
        }