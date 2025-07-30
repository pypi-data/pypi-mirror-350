"""Shims to allow compat between different PyTorch/Lightning versions."""

from __future__ import annotations

from collections.abc import Callable
import logging
import os
from typing import IO, Any, BinaryIO, Optional, Union

from packaging.version import Version, parse as version_parse
import pytorch_lightning
import torch
from typing_extensions import TypeAlias

# These are backported from torch.serialization.py v1.13+
FILE_LIKE: TypeAlias = Union[str, os.PathLike, BinaryIO, IO[bytes]]
MAP_LOCATION: TypeAlias = Optional[
    Union[
        Callable[[torch.Tensor, str], torch.Tensor], torch.device, str, dict[str, str]
    ]
]

_TORCH_VERSION: Version = version_parse(torch.__version__)
_LIGHTNING_VERSION: Version = version_parse(pytorch_lightning.__version__)


_logger = logging.getLogger(__name__)


if _LIGHTNING_VERSION < Version("1.9.0"):
    from pytorch_lightning.loggers import (  # type: ignore[attr-defined] # Reason: Older versions of Lightning _do_ have this attr # noqa: E501
        LightningLoggerBase as LightningLoggerBase,
    )
else:
    from pytorch_lightning.loggers import Logger as LightningLoggerBase  # noqa: F401


if _TORCH_VERSION >= Version("1.13"):
    # This signature matches torch.load() from v1.13+
    def torch_load(
        f: FILE_LIKE,
        map_location: MAP_LOCATION = None,
        pickle_module: Any = None,
        *,
        weights_only: bool = True,
        **pickle_load_args: Any,
    ) -> Any:
        """See torch.load() (>=1.13) for documentation."""
        if not weights_only:
            _logger.warning(
                f"The weights_only argument is currently {weights_only}."
                f" Ensure that what is being loaded in this `torch_load()` call"
                f" is from a trusted source."
            )
        return torch.load(  # nosec[pytorch_load] # See logging above; most pathways are weight_only=True enforced # noqa: E501
            f,
            map_location,
            pickle_module,
            weights_only=weights_only,
            **pickle_load_args,
        )

else:  # torch < 1.13
    # This signature matches torch.load() from v1.13+
    def torch_load(
        f: FILE_LIKE,
        map_location: MAP_LOCATION = None,
        pickle_module: Any = None,
        *,
        weights_only: bool = True,
        **pickle_load_args: Any,
    ) -> Any:
        """See torch.load() (>=1.8.1, <1.13) for documentation."""
        # The signature for torch.load() in <1.13 is:
        # def load(f, map_location=None, pickle_module=pickle, **pickle_load_args)[ -> Any]  # noqa: E501
        # So need to make it match
        if pickle_module is None:
            # TODO: [BIT-987] Review use of pickle
            import pickle  # nosec B403 # import_pickle

            pickle_module = pickle

        if weights_only:
            _logger.warning(
                "The weights_only kwarg is not supported in this version of torch. "
                "This can lead to arbitrary code execution if you are loading an "
                "untrusted model. Please upgrade to torch>=1.13."
            )

        return torch.load(f, map_location, pickle_module, **pickle_load_args)  # nosec[pytorch_load] # weights_only is not supported in this version and we log this fact above # noqa: E501
