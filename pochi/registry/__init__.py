"""レジストリモジュール."""

from .interfaces import IRegistry
from .registry import Registry

__all__ = ["IRegistry", "Registry"]
