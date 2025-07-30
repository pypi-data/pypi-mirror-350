from ._torch_commons import *


def sin_tensor(x: Tensor, freq: float = 1.0) -> Tensor:
    """Applies sine function element-wise."""
    return torch.sin(x * freq)


def cos_tensor(x: Tensor, freq: float = 1.0) -> Tensor:
    """Applies cosine function element-wise."""
    return torch.cos(x * freq)


def sin_plus_cos(x: Tensor, freq: float = 1.0) -> Tensor:
    """Returns sin(x) + cos(x)."""
    return torch.sin(x * freq) + torch.cos(x * freq)


def sin_times_cos(x: Tensor, freq: float = 1.0) -> Tensor:
    """Returns sin(x) * cos(x)."""
    return torch.sin(x * freq) * torch.cos(x * freq)


def apply_window(x: Tensor, window_type: str = "hann") -> Tensor:
    """Applies a window function to a 1D tensor."""
    if window_type == "hann":
        window = torch.hann_window(x.shape[-1], device=x.device)
    elif window_type == "hamming":
        window = torch.hamming_window(x.shape[-1], device=x.device)
    else:
        raise ValueError(f"Unsupported window type: {window_type}")
    return x * window


def shift_ring(x: Tensor, dim: int = -1) -> Tensor:
    """Circularly shifts tensor values: last becomes first (along given dim)."""
    return torch.roll(x, shifts=1, dims=dim)


def dot_product(x: Tensor, y: Tensor, dim: int = -1) -> Tensor:
    """Computes dot product along the specified dimension."""
    return torch.sum(x * y, dim=dim)


def normalize_tensor(x: Tensor, eps: float = 1e-8) -> Tensor:
    """Normalizes a tensor to unit norm (L2)."""
    return x / (torch.norm(x, dim=-1, keepdim=True) + eps)




def log_magnitude(stft_complex: Tensor, eps: float = 1e-5) -> Tensor:
    """Returns log magnitude from complex STFT."""
    magnitude = torch.abs(stft_complex)
    return torch.log(magnitude + eps)


def phase(stft_complex: Tensor) -> Tensor:
    """Returns phase from complex STFT."""
    return torch.angle(stft_complex)
