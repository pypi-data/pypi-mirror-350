from .._torch_commons import *
from .._basics import Model
from ..transform import get_sinusoidal_embedding


class FeedForward(Model):
    def __init__(
        self,
        d_model: int,
        ff_dim: int,
        dropout: float = 0.01,
        activation: nn.Module = nn.LeakyReLU(0.1),
        normalizer: nn.Module = nn.Identity(),
    ):
        """Creates a Feed-Forward Layer, with the chosen activation function and the normalizer."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, ff_dim),
            activation,
            nn.Dropout(dropout),
            nn.Linear(ff_dim, d_model),
            normalizer,
        )

    def forward(self, x: Tensor):
        return self.net(x)


class MLP(Model):
    def __init__(
        self,
        d_model: int,
        ff_dim: int,
        n_classes: int,
        dropout: float = 0.01,
        activation: nn.Module = nn.LeakyReLU(0.1),
        normalizer: nn.Module = nn.Identity(),
    ):
        """Creates a MLP block, with the chosen activation function and the normalizer."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, ff_dim),
            activation,
            nn.Dropout(dropout),
            nn.Linear(ff_dim, n_classes),
            normalizer,
        )

    def forward(self, x: Tensor):
        return self.net(x)


class TimestepEmbedder(nn.Module):
    def __init__(self, dim_emb: int, proj_dim: int):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(dim_emb, proj_dim),
            nn.SiLU(),
            nn.Linear(proj_dim, proj_dim),
        )

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        # t: [B] (long)
        emb = get_sinusoidal_embedding(t, self.mlp[0].in_features)  # [B, dim_emb]
        return self.mlp(emb)  # [B, proj_dim]
