# Placeholder for transformer_engine.py
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class ScaledDotProductAttention(nn.Module):
    """
    Attention(Q,K,V) = softmax(QK^T/sqrt(d_k))V
    """

    def __init__(self):
        super().__init__()

    def forward(self, query, key, value, mask=None):

        d_k = key.size(-1)

        scores = torch.matmul(
            query,
            key.transpose(-2, -1)
        ) / math.sqrt(d_k)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        attention_weights = F.softmax(scores, dim=-1)

        output = torch.matmul(
            attention_weights,
            value
        )

        return output, attention_weights


class MultiHeadAttention(nn.Module):

    def __init__(self, d_model=128, num_heads=8):
        super().__init__()

        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        self.q_linear = nn.Linear(d_model, d_model)
        self.k_linear = nn.Linear(d_model, d_model)
        self.v_linear = nn.Linear(d_model, d_model)

        self.out_linear = nn.Linear(d_model, d_model)

        self.attention = ScaledDotProductAttention()

    def split_heads(self, x):

        batch_size = x.size(0)

        x = x.view(
            batch_size,
            -1,
            self.num_heads,
            self.head_dim
        )

        return x.transpose(1, 2)

    def combine_heads(self, x):

        batch_size = x.size(0)

        x = x.transpose(1, 2).contiguous()

        return x.view(
            batch_size,
            -1,
            self.d_model
        )

    def forward(self, query, key, value, mask=None):

        q = self.split_heads(
            self.q_linear(query)
        )

        k = self.split_heads(
            self.k_linear(key)
        )

        v = self.split_heads(
            self.v_linear(value)
        )

        output, attention_weights = self.attention(
            q, k, v, mask
        )

        output = self.combine_heads(output)

        output = self.out_linear(output)

        return output, attention_weights


class PositionalEncoding(nn.Module):

    def __init__(self, d_model, max_len=5000):
        super().__init__()

        pe = torch.zeros(max_len, d_model)

        position = torch.arange(
            0,
            max_len,
            dtype=torch.float
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                d_model,
                2
            ).float()
            * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        pe = pe.unsqueeze(0)

        self.register_buffer("pe", pe)

    def forward(self, x):

        return x + self.pe[:, :x.size(1)]


class FeedForward(nn.Module):

    def __init__(self, d_model=128, hidden_dim=512):
        super().__init__()

        self.fc1 = nn.Linear(
            d_model,
            hidden_dim
        )

        self.fc2 = nn.Linear(
            hidden_dim,
            d_model
        )

    def forward(self, x):

        x = F.relu(
            self.fc1(x)
        )

        x = self.fc2(x)

        return x


class TransformerEncoderBlock(nn.Module):

    def __init__(
        self,
        d_model=128,
        num_heads=8,
        hidden_dim=512,
        dropout=0.1
    ):
        super().__init__()

        self.attention = MultiHeadAttention(
            d_model,
            num_heads
        )

        self.feed_forward = FeedForward(
            d_model,
            hidden_dim
        )

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        attention_output, _ = self.attention(
            x,
            x,
            x
        )

        x = self.norm1(
            x + self.dropout(attention_output)
        )

        ff_output = self.feed_forward(x)

        x = self.norm2(
            x + self.dropout(ff_output)
        )

        return x


class MiniTransformer(nn.Module):

    def __init__(
        self,
        vocab_size=10000,
        d_model=128,
        num_heads=8,
        hidden_dim=512,
        num_layers=2,
        max_len=512
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            vocab_size,
            d_model
        )

        self.position = PositionalEncoding(
            d_model,
            max_len
        )

        self.layers = nn.ModuleList([
            TransformerEncoderBlock(
                d_model,
                num_heads,
                hidden_dim
            )
            for _ in range(num_layers)
        ])

    def forward(self, x):

        x = self.embedding(x)

        x = self.position(x)

        for layer in self.layers:
            x = layer(x)

        return x