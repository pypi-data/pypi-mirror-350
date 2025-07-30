"""Config YAML specification classes related to hub/AM/auth configuration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Callable

import desert
from marshmallow import fields

from bitfount.hub.types import PRODUCTION_AM_URL, PRODUCTION_HUB_URL

_logger = logging.getLogger(__name__)


@dataclass
class AccessManagerConfig:
    """Configuration for the access manager."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_AM_URL)


@dataclass
class HubConfig:
    """Configuration for the hub."""

    url: str = desert.field(fields.URL(), default=PRODUCTION_HUB_URL)


@dataclass
class APIKeys:
    """API keys for BitfountSession."""

    access_key_id: str = desert.field(fields.String())
    access_key: str = desert.field(fields.String())


@dataclass
class JWT:
    """Externally managed JWT for BitfountSession."""

    jwt: str = desert.field(fields.String())
    expires: datetime = desert.field(fields.DateTime())
    get_token: Callable[[], tuple[str, datetime]] = desert.field(fields.Function())
