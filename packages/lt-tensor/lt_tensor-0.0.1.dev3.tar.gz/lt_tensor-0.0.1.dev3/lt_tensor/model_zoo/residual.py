from .._torch_commons import *
from .._basics import Model
import math
from ..misc_utils import log_tensor


def initialize__weights(model: nn.Module, method: str = "xavier"):
    """Initialize model weights using specified method."""
    for name, param in model.named_parameters():
        if "weight" in name:
            if method == "xavier":
                nn.init.xavier_uniform_(param)
            elif method == "kaiming":
                nn.init.kaiming_uniform_(param, nonlinearity="relu")
        elif "bias" in name:
            nn.init.constant_(param, 0)


def spectral_norm_select(module: Module, enabled: bool):
    if enabled:
        return spectral_norm(module)
    return module


def init_weights(m, mean=0.0, std=0.01):
    classname = m.__class__.__name__
    if "Conv" in classname:
        m.weight.data.normal_(mean, std)


class ResBlock1D(Model):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        dilation: Union[Sequence[int], int] = (1, 3, 5),
        activation: nn.Module = nn.LeakyReLU(0.1),
        num_groups: int = 1,
        batched: bool = True,
    ):
        super().__init__()
        self.conv = nn.ModuleList()
        if isinstance(dilation, int):
            dilation = [dilation]

        if batched:
            layernorm_fn = lambda x: nn.GroupNorm(num_groups=num_groups, num_channels=x)
        else:
            layernorm_fn = lambda x: nn.LayerNorm(normalized_shape=x)
        for i, dil in enumerate(dilation):

            self.conv.append(
                nn.ModuleDict(
                    dict(
                        net=nn.Sequential(
                            self._get_conv_layer(
                                in_channels, in_channels, kernel_size, dil
                            ),
                            activation,
                            self._get_conv_layer(
                                in_channels, in_channels, kernel_size, 1, True
                            ),
                            activation,
                        ),
                        l_norm=layernorm_fn(in_channels),
                    )
                )
            )
        self.final = nn.Sequential(
            self._get_conv_layer(in_channels, out_channels, kernel_size, 1, True),
            activation,
        )
        self.conv.apply(init_weights)

    def _get_conv_layer(
        self,
        channels_in: int,
        channels_out: int,
        kernel_size: int,
        dilation: int,
        pad_gate: bool = False,
    ):
        return weight_norm(
            nn.Conv1d(
                in_channels=channels_in,
                out_channels=channels_out,
                kernel_size=kernel_size,
                stride=1,
                dilation=dilation,
                padding=(
                    int((kernel_size * dilation - dilation) / 2)
                    if not pad_gate
                    else int((kernel_size * 1 - 1) / 2)
                ),
            )
        )

    def forward(self, x: Tensor):
        for i, layer in enumerate(self.conv):
            xt = layer["net"](x)
            x = xt + x
            x = layer["l_norm"](x)
        return self.final(x)

    def remove_weight_norm(self):
        for module in self.modules():
            try:
                remove_weight_norm(module)
            except ValueError:
                pass  # Not normed, skip


class ResBlock2D(Model):
    def __init__(
        self,
        in_channels,
        out_channels,
        downsample=False,
        spec_norm: bool = False,
    ):
        super().__init__()
        stride = 2 if downsample else 1

        self.block = nn.Sequential(
            spectral_norm_select(
                nn.Conv2d(in_channels, out_channels, 3, stride, 1), spec_norm
            ),
            nn.LeakyReLU(0.2),
            spectral_norm_select(
                nn.Conv2d(out_channels, out_channels, 3, 1, 1), spec_norm
            ),
        )

        self.skip = nn.Identity()
        if downsample or in_channels != out_channels:
            self.skip = spectral_norm_select(
                nn.Conv2d(in_channels, out_channels, 1, stride), spec_norm
            )
        # on less to be handled every cicle
        self.sqrt_2 = math.sqrt(2)

    def forward(self, x):
        return (self.block(x) + self.skip(x)) / self.sqrt_2


class ResBlock1DT(Model):
    """For time based residual layers"""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        dilation: Union[Sequence[int], int] = (1, 3, 5),
        activation: nn.Module = nn.LeakyReLU(0.1),
        num_groups: int = 1,
        time_emb_dim: int = 1,
        batched: bool = True,
    ):
        super().__init__()
        self.conv = nn.ModuleList()
        if isinstance(dilation, int):
            dilation = [dilation]
        self.time_proj = nn.Linear(time_emb_dim, out_channels)
        if batched:
            layernorm_fn = lambda x: nn.GroupNorm(num_groups=num_groups, num_channels=x)
        else:
            layernorm_fn = lambda x: nn.LayerNorm(normalized_shape=x)
        for i, dil in enumerate(dilation):

            self.conv.append(
                nn.ModuleDict(
                    dict(
                        net=nn.Sequential(
                            self._get_conv_layer(
                                in_channels, in_channels, kernel_size, dil
                            ),
                            activation,
                            self._get_conv_layer(
                                in_channels, in_channels, kernel_size, 1, True
                            ),
                            activation,
                        ),
                        l_norm=layernorm_fn(in_channels),
                    )
                )
            )
        self.final = nn.Sequential(
            self._get_conv_layer(in_channels, out_channels, kernel_size, 1, True),
            activation,
        )
        self.conv.apply(init_weights)

    def _get_conv_layer(
        self,
        channels_in: int,
        channels_out: int,
        kernel_size: int,
        dilation: int,
        pad_gate: bool = False,
    ):
        return weight_norm(
            nn.Conv1d(
                in_channels=channels_in,
                out_channels=channels_out,
                kernel_size=kernel_size,
                stride=1,
                dilation=dilation,
                padding=(
                    int((kernel_size * dilation - dilation) / 2)
                    if not pad_gate
                    else int((kernel_size * 1 - 1) / 2)
                ),
            )
        )

    def forward(self, x: Tensor, t_embed: Optional[Tensor] = None):
        if t_embed is not None:
            t_emb = self.time_proj(t_embed).unsqueeze(-1)  # [B, C, 1]

        for i, layer in enumerate(self.conv):
            if t_embed is not None:
                xt = layer["net"](x) + t_emb
            else:
                xt = layer["net"](x)
            x = xt + x
            x = layer["l_norm"](x)
        return self.final(x)

    def remove_weight_norm(self):
        for module in self.modules():
            try:
                remove_weight_norm(module)
            except ValueError:
                pass  # Not normed, skip
