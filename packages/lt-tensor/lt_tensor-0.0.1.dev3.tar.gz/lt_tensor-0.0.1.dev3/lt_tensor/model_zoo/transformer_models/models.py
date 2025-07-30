import math
from ..._torch_commons import *
from ..._basics import Model
from lt_utils.misc_utils import default

from .positional_encoders import *
from ..basic import FeedForward


def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.xavier_uniform_(module.weight)
        if module.bias is not None:
            nn.init.constant_(module.bias, 0)
    elif isinstance(module, nn.Embedding):
        nn.init.normal_(module.weight, mean=0.0, std=0.02)
    elif isinstance(module, nn.LayerNorm):
        nn.init.constant_(module.bias, 0)
        nn.init.constant_(module.weight, 1.0)


class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model: int, n_heads: int, ff_size: int, dropout: float = 0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(
            d_model, n_heads, dropout=dropout, batch_first=True
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.ff = FeedForward(d_model, ff_size, dropout)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor, src_mask: Optional[Tensor] = None) -> Tensor:
        attn_output, _ = self.self_attn(x, x, x, attn_mask=src_mask)
        x = self.norm1(x + self.dropout(attn_output))
        ff_output = self.ff(x)
        x = self.norm2(x + self.dropout(ff_output))
        return x


class TransformerDecoderLayer(nn.Module):
    def __init__(self, d_model: int, n_heads: int, ff_size: int, dropout: float = 0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(
            d_model, n_heads, dropout=dropout, batch_first=True
        )
        self.norm1 = nn.LayerNorm(d_model)

        self.cross_attn = nn.MultiheadAttention(
            d_model, n_heads, dropout=dropout, batch_first=True
        )
        self.norm2 = nn.LayerNorm(d_model)

        self.ff = FeedForward(d_model, ff_size, dropout)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self,
        x: Tensor,  # Decoder input [B, T, d_model]
        encoder_out: Tensor,  # Encoder output [B, S, d_model]
        tgt_mask: Optional[Tensor] = None,
        memory_mask: Optional[Tensor] = None,
    ) -> Tensor:
        # 1. Masked Self-Attention
        attn_output, _ = self.self_attn(x, x, x, attn_mask=tgt_mask)
        x = self.norm1(x + self.dropout(attn_output))

        # 2. Cross-Attention
        cross_output, _ = self.cross_attn(
            x, encoder_out, encoder_out, attn_mask=memory_mask
        )
        x = self.norm2(x + self.dropout(cross_output))

        # 3. FeedForward
        ff_output = self.ff(x)
        x = self.norm3(x + self.dropout(ff_output))
        return x


class TransformerEncoder(Model):
    def __init__(
        self,
        d_model: int = 64,
        n_heads: int = 4,
        ff_size: int = 256,
        num_layers: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.layers = nn.ModuleList(
            [
                TransformerEncoderLayer(d_model, n_heads, ff_size, dropout)
                for _ in range(num_layers)
            ]
        )

    def forward(self, x: Tensor, src_mask: Optional[Tensor] = None) -> Tensor:

        for layer in self.layers:
            x = layer(x, src_mask)
        return x


class TransformerDecoder(Model):
    def __init__(
        self,
        d_model: int = 64,
        n_heads: int = 2,
        ff_size: int = 256,
        num_layers: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()

        self.layers = nn.ModuleList(
            [
                TransformerDecoderLayer(d_model, n_heads, ff_size, dropout)
                for _ in range(num_layers)
            ]
        )

    def forward(
        self,
        x: Tensor,
        encoder_out: Tensor,
        tgt_mask: Optional[Tensor] = None,
        memory_mask: Optional[Tensor] = None,
    ) -> Tensor:
        for layer in self.layers:
            x = layer(x, encoder_out, tgt_mask, memory_mask)
        return x
