__all__ = [
    "Downsample1D",
    "Upsample1D",
    "DiffusionUNet",
    "UNetConvBlock1D",
    "UNetUpBlock1D",
    "NoisePredictor1D",
]

from .._torch_commons import *
from .._basics import Model
from .rsd import ResBlock1D
from ..misc_utils import log_tensor


class Downsample1D(Model):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
    ):
        super().__init__()
        self.pool = nn.Conv1d(in_channels, out_channels, 4, stride=2, padding=1)

    def forward(self, x):
        return self.pool(x)


class Upsample1D(Model):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        activation=nn.ReLU(inplace=True),
    ):
        super().__init__()
        self.up = nn.Sequential(
            nn.ConvTranspose1d(
                in_channels, out_channels, kernel_size=4, stride=2, padding=1
            ),
            nn.BatchNorm1d(out_channels),
            activation,
        )

    def forward(self, x):
        return self.up(x)


class DiffusionUNet(Model):
    def __init__(self, in_channels=1, base_channels=64, out_channels=1, depth=4):
        super().__init__()

        self.depth = depth
        self.encoder_blocks = nn.ModuleList()
        self.downsamples = nn.ModuleList()
        self.upsamples = nn.ModuleList()
        self.decoder_blocks = nn.ModuleList()
        # Keep track of channel sizes per layer for skip connections
        self.channels = [in_channels]  # starting input channel
        for i in range(depth):
            enc_in = self.channels[-1]
            enc_out = base_channels * (2**i)
            # Encoder block and downsample
            self.encoder_blocks.append(ResBlock1D(enc_in, enc_out))
            self.downsamples.append(
                Downsample1D(enc_out, enc_out)
            )  # halve time, keep channels
            self.channels.append(enc_out)
        # Bottleneck
        bottleneck_ch = self.channels[-1]
        self.bottleneck = ResBlock1D(bottleneck_ch, bottleneck_ch)
        # Decoder blocks (reverse channel flow)
        for i in reversed(range(depth)):
            skip_ch = self.channels[i + 1]  # from encoder
            dec_out = self.channels[i]  # match earlier stage's output
            self.upsamples.append(Upsample1D(skip_ch, skip_ch))
            self.decoder_blocks.append(ResBlock1D(skip_ch * 2, dec_out))
        # Final output projection (out_channels)
        self.final = nn.Conv1d(in_channels, out_channels, kernel_size=1)

    def forward(self, x: Tensor):
        skips = []

        # Encoder
        for enc, down in zip(self.encoder_blocks, self.downsamples):
            # log_tensor(x, "before enc")
            x = enc(x)
            skips.append(x)
            x = down(x)

        # Bottleneck
        x = self.bottleneck(x)

        # Decoder
        for up, dec, skip in zip(self.upsamples, self.decoder_blocks, reversed(skips)):
            x = up(x)

            # Match lengths via trimming or padding
            if x.shape[-1] > skip.shape[-1]:
                x = x[..., : skip.shape[-1]]
            elif x.shape[-1] < skip.shape[-1]:
                diff = skip.shape[-1] - x.shape[-1]
                x = F.pad(x, (0, diff))

            x = torch.cat([x, skip], dim=1)  # concat on channels
            x = dec(x)

        # Final 1x1 conv
        return self.final(x)


class UNetConvBlock1D(Model):
    def __init__(self, in_channels: int, out_channels: int, down: bool = True):
        super().__init__()
        self.down = down
        self.conv = nn.Sequential(
            nn.Conv1d(
                in_channels,
                out_channels,
                kernel_size=3,
                stride=2 if down else 1,
                padding=1,
            ),
            nn.BatchNorm1d(out_channels),
            nn.LeakyReLU(0.2),
            nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.LeakyReLU(0.2),
        )
        self.downsample = (
            nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=2 if down else 1)
            if in_channels != out_channels
            else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, C, T]
        residual = self.downsample(x)
        return self.conv(x) + residual


class UNetUpBlock1D(Model):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.LeakyReLU(0.2),
            nn.Conv1d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(out_channels),
            nn.LeakyReLU(0.2),
        )
        self.upsample = nn.Upsample(scale_factor=2, mode="nearest")

    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.upsample(x)
        x = torch.cat([x, skip], dim=1)  # skip connection
        return self.conv(x)


class NoisePredictor1D(Model):
    def __init__(self, in_channels: int, cond_dim: int = 0, hidden: int = 128):
        """
        Args:
            in_channels: channels of the noisy input [B, C, T]
            cond_dim: optional condition vector [B, cond_dim]
        """
        super().__init__()
        self.proj = nn.Linear(cond_dim, hidden) if cond_dim > 0 else None
        self.net = nn.Sequential(
            nn.Conv1d(in_channels, hidden, kernel_size=3, padding=1),
            nn.SiLU(),
            nn.Conv1d(hidden, in_channels, kernel_size=3, padding=1),
        )

    def forward(self, x: torch.Tensor, cond: Optional[torch.Tensor] = None):
        # x: [B, C, T], cond: [B, cond_dim]
        if cond is not None:
            cond_proj = self.proj(cond).unsqueeze(-1)  # [B, hidden, 1]
            x = x + cond_proj  # simple conditioning
        return self.net(x)  # [B, C, T]
