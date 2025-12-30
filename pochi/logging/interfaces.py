"""Logging interfaces module.

ロガー関連のインターフェース定義.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path


class ILoggerFactory(ABC):
    """ロガー生成のインターフェース."""

    @abstractmethod
    def create(
        self,
        name: str,
        log_dir: str | Path | None = None,
        level: int = logging.INFO,
    ) -> logging.Logger:
        """ロガーを生成.

        Args:
            name: ロガー名.
            log_dir: ログファイル出力先ディレクトリ. Noneの場合はコンソールのみ.
            level: ログレベル.

        Returns:
            設定済みのロガー.
        """
        ...
