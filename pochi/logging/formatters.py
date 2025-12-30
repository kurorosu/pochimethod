"""Logging formatters module.

ログフォーマッターの定義.
"""

import logging

# デフォルトのログフォーマット
DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# カラーコード
COLORS = {
    "DEBUG": "\033[36m",  # シアン
    "INFO": "\033[32m",  # 緑
    "WARNING": "\033[33m",  # 黄
    "ERROR": "\033[31m",  # 赤
    "CRITICAL": "\033[35m",  # マゼンタ
}
RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """色付きログフォーマッター.

    コンソール出力用にログレベルに応じた色を付与.
    """

    def __init__(
        self,
        fmt: str = DEFAULT_FORMAT,
        datefmt: str = DEFAULT_DATE_FORMAT,
    ) -> None:
        """ColoredFormatterを初期化."""
        super().__init__(fmt, datefmt)

    def format(self, record: logging.LogRecord) -> str:
        """ログレコードをフォーマット."""
        # 元のlevelname を保存
        original_levelname = record.levelname

        # 色を付与
        color = COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{RESET}"

        # フォーマット
        result = super().format(record)

        # 元に戻す
        record.levelname = original_levelname

        return result


class PlainFormatter(logging.Formatter):
    """プレーンテキストフォーマッター.

    ファイル出力用に色なしのフォーマット.
    """

    def __init__(
        self,
        fmt: str = DEFAULT_FORMAT,
        datefmt: str = DEFAULT_DATE_FORMAT,
    ) -> None:
        """PlainFormatterを初期化."""
        super().__init__(fmt, datefmt)
