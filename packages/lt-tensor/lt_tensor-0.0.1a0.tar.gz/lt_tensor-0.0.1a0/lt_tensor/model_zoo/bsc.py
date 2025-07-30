__all__ = [
    "FeedForward",
    "MLP",
    "TimestepEmbedder",
    "GRUEncoder",
    "ConvBlock1D",
    "TemporalPredictor",
    "StyleEncoder",
    "PatchEmbed1D",
    "MultiScaleEncoder1D",
]

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
    ):
        """Creates a MLP block, with the chosen activation function and the normalizer."""
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, ff_dim),
            activation,
            nn.Dropout(dropout),
            nn.Linear(ff_dim, n_classes),
        )

    def forward(self, x: Tensor):
        return self.net(x)


class TimestepEmbedder(Model):
    def __init__(self, dim_emb: int, proj_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim_emb, proj_dim),
            nn.SiLU(),
            nn.Linear(proj_dim, proj_dim),
        )

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        # t: [B] (long)
        emb = get_sinusoidal_embedding(t, self.net[0].in_features)  # [B, dim_emb]
        return self.net(emb)  # [B, proj_dim]


class GRUEncoder(Model):
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        num_layers: int = 1,
        bidirectional: bool = False,
    ):
        super().__init__()
        self.gru = nn.GRU(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
        )
        self.output_dim = hidden_dim * (2 if bidirectional else 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, input_dim]
        output, _ = self.gru(x)  # output: [B, T, hidden_dim*D]
        return output


class ConvBlock1D(Model):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        stride: int = 1,
        norm: bool = True,
        residual: bool = False,
    ):
        super().__init__()
        padding = (kernel_size - 1) // 2
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding)
        self.norm = nn.BatchNorm1d(out_channels) if norm else nn.Identity()
        self.act = nn.LeakyReLU(0.1)
        self.residual = residual and in_channels == out_channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.act(self.norm(self.conv(x)))
        return x + y if self.residual else y


class TemporalPredictor(Model):
    def __init__(
        self,
        d_model: int,
        hidden_dim: int = 128,
        n_layers: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()
        layers = []
        for _ in range(n_layers):
            layers.append(nn.Conv1d(d_model, hidden_dim, kernel_size=3, padding=1))
            layers.append(nn.ReLU())
            layers.append(nn.LayerNorm(hidden_dim))
            layers.append(nn.Dropout(dropout))
            d_model = hidden_dim
        self.network = nn.Sequential(*layers)
        self.proj = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, D]
        x = x.transpose(1, 2)  # [B, D, T]
        x = self.network(x)  # [B, H, T]
        x = x.transpose(1, 2)  # [B, T, H]
        return self.proj(x).squeeze(-1)  # [B, T]


class StyleEncoder(Model):
    def __init__(self, in_channels: int = 80, hidden: int = 128, out_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(in_channels, hidden, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv1d(hidden, hidden, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
        )
        self.linear = nn.Linear(hidden, out_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, Mels, T]
        x = self.net(x).squeeze(-1)  # [B, hidden]
        return self.linear(x)  # [B, out_dim]


class PatchEmbed1D(Model):
    def __init__(self, in_channels: int, patch_size: int, embed_dim: int):
        """
        Args:
            in_channels: number of input channels (e.g., mel bins)
            patch_size: number of time-steps per patch
            embed_dim: dimension of the patch embedding
        """
        super().__init__()
        self.patch_size = patch_size
        self.proj = nn.Conv1d(
            in_channels, embed_dim, kernel_size=patch_size, stride=patch_size
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, T]
        x = self.proj(x)  # [B, embed_dim, T//patch_size]
        return x.transpose(1, 2)  # [B, T_patches, embed_dim]


class MultiScaleEncoder1D(Model):
    def __init__(
        self, in_channels: int, hidden: int, num_layers: int = 4, kernel_size: int = 3
    ):
        super().__init__()
        layers = []
        for i in range(num_layers):
            layers.append(
                nn.Conv1d(
                    in_channels if i == 0 else hidden,
                    hidden,
                    kernel_size=kernel_size,
                    dilation=2**i,
                    padding=(kernel_size - 1) * (2**i) // 2,
                )
            )
            layers.append(nn.GELU())
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, T]
        return self.net(x)  # [B, hidden, T]
