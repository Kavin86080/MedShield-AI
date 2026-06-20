from multimodal.pdf_processor import (
    PDFProcessor
)

from rag.chunkers.text_chunker import (
    TextChunker
)

from rag.retrievers.dense_retriever import (
    DenseRetriever
)


class PDFRAGPipeline:

    def __init__(self):

        self.pdf_processor = (
            PDFProcessor()
        )

        self.chunker = (
            TextChunker()
        )

        self.retriever = (
            DenseRetriever()
        )

    def index_pdf(
        self,
        pdf_path
    ):

        text = (
            self.pdf_processor.extract_text(
                pdf_path
            )
        )

        chunks = (
            self.chunker.chunk(
                text
            )
        )

        self.retriever.index_documents(
            chunks
        )

        return len(chunks)

    def query(
        self,
        question,
        top_k=3
    ):

        return self.retriever.retrieve(
            query=question,
            top_k=top_k
        )