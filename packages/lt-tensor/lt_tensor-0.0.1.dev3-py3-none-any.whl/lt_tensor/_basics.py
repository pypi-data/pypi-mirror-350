__all__ = ["Model"]


import warnings
from ._torch_commons import *

ROOT_DEVICE = torch.device(torch.zeros(1).device)

class _ModelDevice(nn.Module):
    """
    This makes it easier to assign a device and retrieves it later
    """

    _device: torch.device = ROOT_DEVICE

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, device: Union[torch.device, str]):
        assert isinstance(device, (str, torch.device))
        self._device = torch.device(device) if isinstance(device, str) else device
        self.tp_apply_device_to()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tp_apply_device_to(self):
        """Add here components that are needed to have device applied to them,
        that usualy the '.to()' function fails to apply

        example:
        ```
        def tp_apply_device_to(self):
            self.my_tensor = self.my_tensor.to(device=self.device)
        ```
        """
        pass

    def to(self, *args, **kwargs):
        device, dtype, non_blocking, convert_to_format = torch._C._nn._parse_to(
            *args, **kwargs
        )

        if dtype is not None:
            if not (dtype.is_floating_point or dtype.is_complex):
                raise TypeError(
                    "nn.Module.to only accepts floating point or complex "
                    f"dtypes, but got desired dtype={dtype}"
                )
            if dtype.is_complex:
                warnings.warn(
                    "Complex modules are a new feature under active development whose design may change, "
                    "and some modules might not work as expected when using complex tensors as parameters or buffers. "
                    "Please file an issue at https://github.com/pytorch/pytorch/issues/new?template=bug-report.yml "
                    "if a complex module does not work as expected."
                )

        def convert(t: Tensor):
            try:
                if convert_to_format is not None and t.dim() in (4, 5):
                    return t.to(
                        device,
                        dtype if t.is_floating_point() or t.is_complex() else None,
                        non_blocking,
                        memory_format=convert_to_format,
                    )
                return t.to(
                    device,
                    dtype if t.is_floating_point() or t.is_complex() else None,
                    non_blocking,
                )
            except NotImplementedError as e:
                if str(e) == "Cannot copy out of meta tensor; no data!":
                    raise NotImplementedError(
                        f"{e} Please use torch.nn.Module.to_empty() instead of torch.nn.Module.to() "
                        f"when moving module from meta to a different device."
                    ) from None
                else:
                    raise

        self._apply(convert)
        self.device = device
        return self

    def ipu(self, device: Optional[Union[int, torch.device]] = None) -> T:
        super().ipu(device)
        dvc = "ipu"
        if device is not None:
            dvc += (
                ":" + str(device) if isinstance(device, (int, float)) else device.index
            )
        self.device = dvc
        return self

    def xpu(self, device: Optional[Union[int, torch.device]] = None) -> T:
        super().xpu(device)
        dvc = "xpu"
        if device is not None:
            dvc += (
                ":" + str(device) if isinstance(device, (int, float)) else device.index
            )
        self.device = dvc
        return self

    def cuda(self, device: Optional[Union[int, torch.device]] = None) -> T:
        super().cuda(device)
        dvc = "cuda"
        if device is not None:
            dvc += (
                ":" + str(device) if isinstance(device, (int, float)) else device.index
            )
        self.device = dvc
        return self

    def mtia(self, device: Optional[Union[int, torch.device]] = None) -> T:
        super().mtia(device)
        dvc = "mtia"
        if device is not None:
            dvc += (
                ":" + str(device) if isinstance(device, (int, float)) else device.index
            )
        self.device = dvc
        return self

    def cpu(self) -> T:
        super().cpu()
        self.device = "cpu"
        return self


class Model(_ModelDevice, ABC):
    """
    For easier access of items in a model
    This applies to all except to "forward", "save_weights", "load_weights",
    "train_step", and "inference".
    """

    _autocast: bool = False

    @property
    def autocast(self):
        return self._autocast

    @autocast.setter
    def autocast(self, value: bool):
        self._autocast = value

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        device = kwargs.get("device", None)
        if isinstance(device, (torch.device, str)):
            self.to(device)
        self.autocast = kwargs.get("autocast", self.autocast)

    def tp_count_parameters(self, module_name: Optional[str] = None):
        """Gets the numer of parameters from either the entire model or from a specific module"""
        if module_name is not None:
            assert hasattr(self, module_name), f"Module {module_name} does not exits"
            module = getattr(self, module_name)
            return sum([x.numel() for x in module.parameters()])
        else:
            return sum([x.numel() for x in self.parameters()])

    def tp_get_weights(self, module_name: Optional[str] = None) -> List[Tensor]:
        """Returns the weights of the model entrie model or from a specified module"""
        if module_name is not None:
            assert hasattr(self, module_name), f"Module {module_name} does not exits"
            module = getattr(self, module_name)
            return [x.data.detach() for x in module.parameters()]
        return [x.data.detach() for x in self.parameters()]

    def tp_print_num_params(self, module_name: Optional[str] = None) -> List[Tensor]:
        params = format(self.tp_count_parameters(module_name), ",").replace(",", ".")

        if module_name:
            print(f'Parameters from "{module_name}": {params}')
        else:
            print(f"Parameters: {params}")

    def save_weights(self, path: Union[Path, str]):
        path = Path(path)
        if path.exists():
            assert (
                path.is_file()
            ), "The provided path exists but its a directory not a file!"
            path.rmdir()
        path.parent.mkdir(exist_ok=True, parents=True)
        torch.save(obj=self.state_dict(), f=str(path))

    def load_weights(
        self,
        path: Union[Path, str],
        raise_if_not_exists: bool = False,
        strict: bool = True,
        assign: bool = False,
        weights_only: bool = False,
        mmap: Optional[bool] = None,
        **torch_loader_kwargs,
    ):
        path = Path(path)
        if not path.exists():
            assert not raise_if_not_exists, "Path does not exists!"
            return None
        assert path.is_file(), "The provided path is not a valid file!"
        state_dict = torch.load(
            str(path), weights_only=weights_only, mmap=mmap, **torch_loader_kwargs
        )
        incompatible_keys = self.load_state_dict(
            state_dict,
            strict=strict,
            assign=assign,
        )
        return incompatible_keys

    @torch.no_grad()
    def inference(self, *args, **kwargs):
        if self.training:
            self.eval()
        if self.autocast:
            with torch.autocast(device_type=self.device.type):
                return self(*args, **kwargs)
        return self(*args, **kwargs)

    def train_step(
        self,
        *args,
        **kwargs,
    ):
        """Train Step"""
        if not self.training:
            self.train()
        return self(*args, **kwargs)

    @abstractmethod
    def forward(
        self, *args, **kwargs
    ) -> Union[Tensor, Sequence[Tensor], Dict[Any, Union[Any, Tensor]]]:
        pass
