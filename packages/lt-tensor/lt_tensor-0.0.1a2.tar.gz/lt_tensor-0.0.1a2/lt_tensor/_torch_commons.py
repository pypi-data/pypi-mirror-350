import torch
import torch.nn.functional as F
from torch.optim import Optimizer
from torch.nn.utils import remove_weight_norm
from torch.nn.utils.parametrizations import weight_norm, spectral_norm
from torch import nn, optim, Tensor, FloatTensor, LongTensor

from lt_utils.common import *

DeviceType: TypeAlias = Union[torch.device, str]
