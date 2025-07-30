"""Base models and helper classes using PyTorch as the backend."""

from __future__ import annotations

import logging
from typing import Union

import torch

# Convention is to import functional as F
# noinspection PyPep8Naming
from torch.nn import functional as F
import torch.optim as optimizers
import torch_optimizer as torch_optimizers

from bitfount.models.base_models import ClassifierMixIn
from bitfount.types import _StrAnyDict
from bitfount.utils import delegates

logger = logging.getLogger(__name__)


_OptimizerType = Union[torch_optimizers.Optimizer, optimizers.Optimizer]
_STEP_OUTPUT = Union[torch.Tensor, _StrAnyDict]  # From pl.LightningModule


@delegates()
class PyTorchClassifierMixIn(ClassifierMixIn):
    """MixIn for PyTorch classification problems.

    PyTorch classification models must have this class in their inheritance hierarchy.
    """

    def _do_output_activation(self, output: torch.Tensor) -> torch.Tensor:
        """Perform final activation function on output."""
        if self.multilabel:
            return torch.sigmoid(output)
        else:
            return F.softmax(output, dim=1)
