# Placeholder for sentence_transformer_embedder.py
from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedder:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(
            model_name
        )

    def embed_text(self, text):

        embedding = self.model.encode(
            text,
            convert_to_tensor=False
        )

        return embedding

    def embed_documents(self, documents):

        embeddings = self.model.encode(
            documents,
            convert_to_tensor=False
        )

        return embeddings