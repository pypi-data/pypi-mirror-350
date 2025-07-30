from ._torch_commons import *
import torchaudio
import math
import random
from .misc_utils import log_tensor


def to_mel_spectrogram(
    waveform: torch.Tensor,
    sample_rate: int = 22050,
    n_fft: int = 1024,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    n_mels: int = 80,
    f_min: float = 0.0,
    f_max: Optional[float] = None,
) -> torch.Tensor:
    """Converts waveform to mel spectrogram."""
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        n_mels=n_mels,
        f_min=f_min,
        f_max=f_max,
    )
    return mel_spectrogram(waveform)


def stft(
    waveform: Tensor,
    n_fft: int = 512,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    window_fn: str = "hann",
    center: bool = True,
    return_complex: bool = True,
) -> Tensor:
    """Performs short-time Fourier transform using PyTorch."""
    window = (
        torch.hann_window(win_length or n_fft).to(waveform.device)
        if window_fn == "hann"
        else None
    )
    return torch.stft(
        input=waveform,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        center=center,
        return_complex=return_complex,
    )


def istft(
    stft_matrix: Tensor,
    n_fft: int = 512,
    hop_length: Optional[int] = None,
    win_length: Optional[int] = None,
    window_fn: str = "hann",
    center: bool = True,
    length: Optional[int] = None,
) -> Tensor:
    """Performs inverse short-time Fourier transform using PyTorch."""
    window = (
        torch.hann_window(win_length or n_fft).to(stft_matrix.device)
        if window_fn == "hann"
        else None
    )
    return torch.istft(
        input=stft_matrix,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        center=center,
        length=length,
    )


def fft(x: Tensor, norm: Optional[str] = "backward") -> Tensor:
    """Returns the FFT of a real tensor."""
    return torch.fft.fft(x, norm=norm)


def ifft(x: Tensor, norm: Optional[str] = "backward") -> Tensor:
    """Returns the inverse FFT of a complex tensor."""
    return torch.fft.ifft(x, norm=norm)


def to_log_mel_spectrogram(
    waveform: torch.Tensor, sample_rate: int = 22050, eps: float = 1e-9, **kwargs
) -> torch.Tensor:
    """Converts waveform to log-mel spectrogram."""
    mel = to_mel_spectrogram(waveform, sample_rate, **kwargs)
    return torch.log(mel + eps)


def normalize(
    x: torch.Tensor,
    mean: Optional[float] = None,
    std: Optional[float] = None,
    eps: float = 1e-9,
) -> torch.Tensor:
    """Normalizes tensor by mean and std."""
    if mean is None:
        mean = x.mean()
    if std is None:
        std = x.std()
    return (x - mean) / (std + eps)


def min_max_scale(
    x: torch.Tensor, min_val: float = 0.0, max_val: float = 1.0
) -> torch.Tensor:
    """Scales tensor to [min_val, max_val] range."""
    x_min, x_max = x.min(), x.max()
    return (x - x_min) / (x_max - x_min + 1e-8) * (max_val - min_val) + min_val


def mel_to_linear(
    mel_spec: torch.Tensor, mel_fb: torch.Tensor, eps: float = 1e-8
) -> torch.Tensor:
    """Approximate inversion of mel to linear spectrogram using pseudo-inverse."""
    mel_fb_inv = torch.pinverse(mel_fb)
    return torch.matmul(mel_fb_inv, mel_spec + eps)


def add_noise(x: torch.Tensor, noise_level: float = 0.01) -> torch.Tensor:
    """Adds Gaussian noise to tensor."""
    return x + noise_level * torch.randn_like(x)


def shift_time(x: torch.Tensor, shift: int) -> torch.Tensor:
    """Shifts tensor along time axis (last dim)."""
    return torch.roll(x, shifts=shift, dims=-1)


def stretch_tensor(x: torch.Tensor, rate: float, mode: str = "linear") -> torch.Tensor:
    """Time-stretch tensor using interpolation."""
    B, C, T = x.shape if x.ndim == 3 else (1, 1, x.shape[0])
    new_T = int(T * rate)
    x_reshaped = x.view(B * C, T).unsqueeze(1)
    stretched = torch.nn.functional.interpolate(x_reshaped, size=new_T, mode=mode)
    return (
        stretched.squeeze(1).view(B, C, new_T) if x.ndim == 3 else stretched.squeeze()
    )


def pad_tensor(
    x: torch.Tensor, target_len: int, pad_value: float = 0.0
) -> torch.Tensor:
    """Pads tensor to target length along last dimension."""
    current_len = x.shape[-1]
    if current_len >= target_len:
        return x[..., :target_len]
    padding = [0] * (2 * (x.ndim - 1)) + [0, target_len - current_len]
    return F.pad(x, padding, value=pad_value)


def get_sinusoidal_embedding(timesteps: torch.Tensor, dim: int) -> torch.Tensor:
    # Expect shape [B] or [B, 1]
    if timesteps.dim() > 1:
        timesteps = timesteps.view(-1)  # flatten to [B]

    device = timesteps.device
    half_dim = dim // 2
    emb = torch.exp(
        torch.arange(half_dim, device=device) * -(math.log(10000.0) / half_dim)
    )
    emb = timesteps[:, None].float() * emb[None, :]  # [B, half_dim]
    emb = torch.cat((emb.sin(), emb.cos()), dim=-1)  # [B, dim]
    return emb


def _generate_window(
    M: int, alpha: float = 0.5, device: Optional[DeviceType] = None
) -> Tensor:
    if M < 1:
        raise ValueError("Window length M must be >= 1.")
    if M == 1:
        return torch.ones(1, device=device)

    n = torch.arange(M, dtype=torch.float32, device=device)
    window = alpha - (1.0 - alpha) * torch.cos(2.0 * math.pi * n / (M - 1))
    return window


def pad_center(tensor: torch.Tensor, size: int, axis: int = -1) -> torch.Tensor:
    n = tensor.shape[axis]
    if size < n:
        raise ValueError(f"Target size ({size}) must be at least input size ({n})")

    lpad = (size - n) // 2
    rpad = size - n - lpad

    pad = [0] * (2 * tensor.ndim)
    pad[2 * axis + 1] = rpad
    pad[2 * axis] = lpad

    return F.pad(tensor, pad, mode="constant", value=0)


def normalize(
    S: torch.Tensor,
    norm: float = float("inf"),
    axis: int = 0,
    threshold: float = 1e-10,
    fill: bool = False,
) -> torch.Tensor:
    mag = S.abs().float()

    if norm is None:
        return S

    elif norm == float("inf"):
        length = mag.max(dim=axis, keepdim=True).values

    elif norm == float("-inf"):
        length = mag.min(dim=axis, keepdim=True).values

    elif norm == 0:
        length = (mag > 0).sum(dim=axis, keepdim=True).float()

    elif norm > 0:
        length = (mag**norm).sum(dim=axis, keepdim=True) ** (1.0 / norm)

    else:
        raise ValueError(f"Unsupported norm: {norm}")

    small_idx = length < threshold
    length = length.clone()
    if fill:
        length[small_idx] = float("nan")
        Snorm = S / length
        Snorm[Snorm != Snorm] = 1.0  # replace nan with fill_norm (default 1.0)
    else:
        length[small_idx] = float("inf")
        Snorm = S / length

    return Snorm


def window_sumsquare(
    window_spec: Union[str, int, float, Callable, List[Any], Tuple[Any, ...]],
    n_frames: int,
    hop_length: int = 300,
    win_length: int = 1200,
    n_fft: int = 2048,
    dtype: torch.dtype = torch.float32,
    norm: Optional[Union[int, float]] = None,
    device: Optional[torch.device] = "cpu",
):
    if win_length is None:
        win_length = n_fft

    total_length = n_fft + hop_length * (n_frames - 1)
    x = torch.zeros(total_length, dtype=dtype, device=device)

    # Get the window (from scipy for now)
    win = _generate_window(window_spec, win_length, fftbins=True)
    win = torch.tensor(win, dtype=dtype, device=device)

    # Normalize and square
    win_sq = normalize(win, norm=norm, axis=0) ** 2
    win_sq = pad_center(win_sq, size=n_fft, axis=0)

    # Accumulate squared windows
    for i in range(n_frames):
        sample = i * hop_length
        end = min(total_length, sample + n_fft)
        length = end - sample
        x[sample:end] += win_sq[:length]

    return x



def inverse_transform(
    spec: Tensor,
    phase: Tensor,
    window: Optional[Tensor] = None,
    n_fft: int = 2048,
    hop_length: int = 300,
    win_length: int = 1200,
    length: Optional[Any] = None,
):
    if window is None:
        window = _generate_window(win_length)
    return torch.istft(
        spec * torch.exp(phase * 1j),
        n_fft,
        hop_length,
        win_length,
        window=window,
        length=length,
    )


def stft_istft_rebuild(
    input_data: Tensor,
    window: Optional[Tensor] = None,
    n_fft: int = 2048,
    hop_length: int = 300,
    win_length: int = 1200,
):
    """
    Perform STFT followed by ISTFT reconstruction using magnitude and phase.
    """
    if window is None:
        window = _generate_window(win_length)
    st = torch.stft(
        input_data,
        n_fft,
        hop_length,
        win_length,
        window=window,
        return_complex=True,
    )
    return torch.istft(
        torch.abs(st) * torch.exp(1j * torch.angle(st)),
        n_fft,
        hop_length,
        win_length,
        window=window,
        length=input_data.shape[-1],
    ).squeeze(0)
