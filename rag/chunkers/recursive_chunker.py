# Placeholder for recursive_chunker.py
class RecursiveChunker:

    def __init__(
        self,
        chunk_size=100,
        overlap=20
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text):

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += (
                self.chunk_size
                - self.overlap
            )

        return chunks