import os
import torch

from ai_engine.transformer_engine.transformer_engine import MiniTransformer


class TransformerService:

    def __init__(
        self,
        vocab_size=10000,
        d_model=128,
        num_heads=8,
        hidden_dim=512,
        num_layers=2,
        max_len=512,
        device="cpu"
    ):

        self.device = device

        self.model = MiniTransformer(
            vocab_size=vocab_size,
            d_model=d_model,
            num_heads=num_heads,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            max_len=max_len
        ).to(device)

    def predict(self, token_ids):

        self.model.eval()

        token_ids = token_ids.to(self.device)

        with torch.no_grad():

            output = self.model(token_ids)

        return output

    def generate_embeddings(self, token_ids):

        embeddings = self.predict(token_ids)

        return embeddings.mean(dim=1)

    def save_model(self, save_path):

        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        torch.save(
            self.model.state_dict(),
            save_path
        )

        return {
            "status": "success",
            "path": save_path
        }

    def load_model(self, model_path):

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=self.device
            )
        )

        self.model.eval()

        return {
            "status": "loaded",
            "path": model_path
        }

    def parameter_count(self):

        return sum(
            p.numel()
            for p in self.model.parameters()
        )

    def model_summary(self):

        return {
            "model": "MiniTransformer",
            "device": self.device,
            "parameters": self.parameter_count(),
            "status": "loaded"
        }