from __future__ import annotations

from enum import Enum


class CredsOrigin(Enum):
    """
    List credential origins.
    """

    ENV = "env"
    FILE = "file"


class SetCreds(Enum):
    """
    List supported environments.
    """

    DEFAULT = "__default"
    DH_ENV = "DH_NAME"
