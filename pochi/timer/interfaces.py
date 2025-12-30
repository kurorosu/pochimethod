"""Timer interfaces module.

タイマー関連のインターフェース定義.
"""

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .timer import TimerContext


class ITimerFactory(ABC):
    """タイマー生成のインターフェース."""

    @abstractmethod
    def create(self, name: str, logger: logging.Logger | None = None) -> "TimerContext":
        """タイマーコンテキストを生成.

        Args:
            name: タイマー名（ログ出力時に使用）.
            logger: ログ出力先. Noneの場合はprint出力.

        Returns:
            コンテキストマネージャーとして使用可能なタイマー.
        """
        ...
