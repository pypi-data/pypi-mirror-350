import torch
from torch import nn, optim
import torch.nn.functional as F
from torch.optim import Optimizer
from torch.nn import Module, L1Loss, MSELoss
from torch.nn.utils import remove_weight_norm
from torch import Tensor, FloatTensor, device, LongTensor
from torch.nn.utils.parametrizations import weight_norm, spectral_norm

from lt_utils.common import *

DeviceType: TypeAlias = Union[device, str]
