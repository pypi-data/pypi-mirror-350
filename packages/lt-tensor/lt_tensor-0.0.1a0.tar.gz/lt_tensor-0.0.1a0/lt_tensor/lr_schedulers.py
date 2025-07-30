__all__ = [
    "WarmupDecayScheduler",
    "AdaptiveDropScheduler",
    "WaveringLRScheduler",
]

import math
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler


class WarmupDecayScheduler(_LRScheduler):
    def __init__(
        self,
        optimizer: Optimizer,
        warmup_steps: int,
        total_steps: int,
        decay_type: str = "linear",  # or "cosine"
        min_lr: float = 0.0,
        last_epoch: int = -1,
    ):
        self.warmup_steps = warmup_steps
        self.total_steps = total_steps
        self.decay_type = decay_type
        self.min_lr = min_lr
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        step = self.last_epoch + 1
        warmup = self.warmup_steps
        total = self.total_steps
        lrs = []

        for base_lr in self.base_lrs:
            if step < warmup:
                lr = base_lr * step / warmup
            else:
                progress = (step - warmup) / max(1, total - warmup)
                if self.decay_type == "linear":
                    lr = base_lr * (1.0 - progress)
                elif self.decay_type == "cosine":
                    lr = base_lr * 0.5 * (1 + math.cos(math.pi * progress))
                else:
                    raise ValueError(f"Unknown decay type: {self.decay_type}")

            lr = max(self.min_lr, lr)
            lrs.append(lr)

        return lrs


class AdaptiveDropScheduler(_LRScheduler):
    def __init__(
        self,
        optimizer,
        drop_factor=0.5,
        patience=10,
        min_lr=1e-6,
        cooldown=5,
        last_epoch=-1,
    ):
        self.drop_factor = drop_factor
        self.patience = patience
        self.min_lr = min_lr
        self.cooldown = cooldown
        self.cooldown_counter = 0
        self.best_loss = float("inf")
        self.bad_steps = 0
        super().__init__(optimizer, last_epoch)

    def step(self, val_loss=None):
        if val_loss is not None:
            if val_loss < self.best_loss:
                self.best_loss = val_loss
                self.bad_steps = 0
                self.cooldown_counter = 0
            else:
                self.bad_steps += 1
                if self.bad_steps >= self.patience and self.cooldown_counter == 0:
                    for i, group in enumerate(self.optimizer.param_groups):
                        new_lr = max(group["lr"] * self.drop_factor, self.min_lr)
                        group["lr"] = new_lr
                    self.cooldown_counter = self.cooldown
                    self.bad_steps = 0
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

    def get_lr(self):
        return [group["lr"] for group in self.optimizer.param_groups]


class WaveringLRScheduler(_LRScheduler):
    def __init__(
        self, optimizer, base_lr, max_lr, period=1000, decay=0.999, last_epoch=-1
    ):
        """
        Sinusoidal-like oscillating LR. Can escape shallow local minima.
        - base_lr: minimum LR
        - max_lr: maximum LR
        - period: full sine cycle in steps
        - decay: multiplies max_lr each cycle
        """
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.period = period
        self.decay = decay
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        cycle = self.last_epoch // self.period
        step_in_cycle = self.last_epoch % self.period
        factor = math.sin(math.pi * step_in_cycle / self.period)
        amplitude = (self.max_lr - self.base_lr) * (self.decay**cycle)
        return [self.base_lr + amplitude * factor for _ in self.optimizer.param_groups]
