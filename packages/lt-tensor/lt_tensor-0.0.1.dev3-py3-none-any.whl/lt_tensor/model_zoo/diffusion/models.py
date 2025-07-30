__all__ = [
    "ResidualBlock1D_B",
    "Downsample1D",
    "Upsample1D",
    "DiffusionUNet",
    "DiffusionUNetT",
]

from ..._torch_commons import *
from ..._basics import Model
from ..residual import ResBlock1D, ResBlock1DT
from ...misc_utils import log_tensor



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





