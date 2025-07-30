__all__ = [
    "ConcatFusion",
    "FiLMFusion",
    "BilinearFusion",
    "CrossAttentionFusion",
    "GatedFusion",
]

from .._torch_commons import *
from .._basics import Model


class ConcatFusion(Model):
    def __init__(self, in_dim_a: int, in_dim_b: int, out_dim: int):
        super().__init__()
        self.proj = nn.Linear(in_dim_a + in_dim_b, out_dim)

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        x = torch.cat([a, b], dim=-1)
        return self.proj(x)


class FiLMFusion(Model):
    def __init__(self, cond_dim: int, feature_dim: int):
        super().__init__()
        self.modulator = nn.Linear(cond_dim, 2 * feature_dim)

    def forward(self, x: Tensor, cond: Tensor) -> Tensor:
        scale, shift = self.modulator(cond).chunk(2, dim=-1)
        return x * scale + shift


class BilinearFusion(Model):
    def __init__(self, in_dim_a: int, in_dim_b: int, out_dim: int):
        super().__init__()
        self.bilinear = nn.Bilinear(in_dim_a, in_dim_b, out_dim)

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        return self.bilinear(a, b)


class CrossAttentionFusion(nn.Module):
    def __init__(self, q_dim: int, kv_dim: int, n_heads: int = 4, d_model: int = 256):
        super().__init__()
        self.q_proj = nn.Linear(q_dim, d_model)
        self.k_proj = nn.Linear(kv_dim, d_model)
        self.v_proj = nn.Linear(kv_dim, d_model)
        self.attn = nn.MultiheadAttention(
            embed_dim=d_model, num_heads=n_heads, batch_first=True
        )

    def forward(self, query: Tensor, context: Tensor, mask: Tensor = None) -> Tensor:
        Q = self.q_proj(query)
        K = self.k_proj(context)
        V = self.v_proj(context)
        output, _ = self.attn(Q, K, V, key_padding_mask=mask)
        return output


class GatedFusion(nn.Module):
    def __init__(self, in_dim: int):
        super().__init__()
        self.gate = nn.Sequential(nn.Linear(in_dim * 2, in_dim), nn.Sigmoid())

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        gate = self.gate(torch.cat([a, b], dim=-1))
        return gate * a + (1 - gate) * b
