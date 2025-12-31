"""Timer implementation module.

タイマーの実装.
"""

import logging
import time
from types import TracebackType

from .interfaces import ITimerFactory


class TimerContext:
    """タイマーコンテキストマネージャー.

    処理時間を計測し、終了時にログ出力.

    Args:
        name: タイマー名.
        logger: ログ出力先. Noneの場合はprint出力.
    """

    def __init__(self, name: str, logger: logging.Logger | None = None) -> None:
        """TimerContextを初期化."""
        self._name = name
        self._logger = logger
        self._start_time: float = 0.0
        self._elapsed: float = 0.0

    def __enter__(self) -> "TimerContext":
        """コンテキスト開始時に呼ばれる."""
        self._start_time = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """コンテキスト終了時に呼ばれる."""
        self._elapsed = time.perf_counter() - self._start_time

        if exc_type is not None:
            # 例外発生時
            message = f"{self._name} (failed): {self._elapsed:.3f}s"
            if self._logger is not None:
                self._logger.warning(message)
            else:
                print(message)
        else:
            # 正常終了時
            message = f"{self._name}: {self._elapsed:.3f}s"
            if self._logger is not None:
                self._logger.info(message)
            else:
                print(message)

    @property
    def elapsed(self) -> float:
        """経過時間（秒）を取得."""
        return self._elapsed


class TimerFactory(ITimerFactory):
    """タイマー生成の実装クラス."""

    def create(
        self,
        name: str,
        logger: logging.Logger | None = None,
    ) -> TimerContext:
        """タイマーコンテキストを生成.

        Args:
            name: タイマー名（ログ出力時に使用）.
            logger: ログ出力先. Noneの場合はprint出力.

        Returns:
            コンテキストマネージャーとして使用可能なタイマー.
        """
        return TimerContext(name, logger=logger)
