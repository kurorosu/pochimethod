"""Logging handlers module.

ログハンドラーの生成関数.
"""

import logging
import sys
from pathlib import Path

from .formatters import ColoredFormatter, PlainFormatter


def create_console_handler(level: int = logging.INFO) -> logging.StreamHandler:
    """色付きコンソールハンドラーを生成.

    Args:
        level: ログレベル.

    Returns:
        設定済みのStreamHandler.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(ColoredFormatter())
    return handler


def create_file_handler(
    log_path: Path,
    level: int = logging.INFO,
) -> logging.FileHandler:
    """ファイルハンドラーを生成.

    Args:
        log_path: ログファイルのパス.
        level: ログレベル.

    Returns:
        設定済みのFileHandler.
    """
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(PlainFormatter())
    return handler
