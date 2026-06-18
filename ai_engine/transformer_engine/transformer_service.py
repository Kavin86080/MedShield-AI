# Placeholder for transformer_service.py
import torch

from ai_engine.transformer_engine.transformer_engine import MiniTransformer


class TransformerService:

    def __init__(self):

        self.model = MiniTransformer()

    def predict(self, token_ids):

        self.model.eval()

        with torch.no_grad():

            output = self.model(token_ids)

        return output

    def model_summary(self):

        return {
            "model": "MiniTransformer",
            "status": "loaded"
        }