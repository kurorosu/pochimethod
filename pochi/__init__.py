"""Pochi - A versatile method collection for Python."""

from .logging import ILoggerFactory
from .pochi import Pochi
from .timer import ITimerFactory
from .workspace import IWorkspaceCreator, Workspace

__version__ = "0.0.1"
__all__ = ["ILoggerFactory", "ITimerFactory", "IWorkspaceCreator", "Pochi", "Workspace"]
