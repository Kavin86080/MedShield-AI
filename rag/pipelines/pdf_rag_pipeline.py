from multimodal.pdf_processor import PDFProcessor
from rag.chunkers.text_chunker import TextChunker
from rag.retrievers.dense_retriever import DenseRetriever


class PDFRAGPipeline:

    def __init__(self):

        self.pdf_processor = PDFProcessor()

        self.chunker = TextChunker()

        self.retriever = DenseRetriever()

    def reset_index(self):

        self.retriever = DenseRetriever()

    def index_pdf(
        self,
        pdf_path,
        reset_index=False
    ):

        text = self.pdf_processor.extract_text(
            pdf_path
        )
        print("\n" + "="*50)
        print("PDF PATH:")
        print(pdf_path)
        print("\nTEXT LENGTH:")
        print(len(text))
        print("\nFIRST 1000 CHARS:")
        import sys
        try:
            encoding = sys.stdout.encoding or 'utf-8'
            print(text[:1000].encode(encoding, errors='replace').decode(encoding))
        except Exception:
            print(text[:1000].encode('ascii', errors='replace').decode('ascii'))
        print("="*50)

        chunks = self.chunker.chunk(
            text
        )

        if reset_index:

            self.reset_index()

        self.retriever.index_documents(
            chunks
        )

        print(
            f"\nIndexed PDF: {pdf_path}"
        )

        print(
            f"Chunks Indexed: {len(chunks)}"
        )

        print(
            f"Total Documents In Store: "
            f"{self.retriever.total_documents()}"
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