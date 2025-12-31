"""Logging factory module.

ロガー生成の実装.
"""

import logging
from pathlib import Path

from .handlers import create_console_handler, create_file_handler
from .interfaces import ILoggerFactory


class LoggerFactory(ILoggerFactory):
    """ロガー生成の実装クラス.

    コンソール出力（色付き）とファイル出力（プレーン）を提供.
    ロガー名には自動的に 'pochi.' プレフィックスが付与され,
    他のライブラリとの名前衝突を防ぐ.
    """

    # 生成済みロガーのキャッシュ
    _loggers: dict[str, logging.Logger] = {}

    # ロガー名のプレフィックス
    _PREFIX = "pochi."

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
        # プレフィックス付きのロガー名を生成
        logger_name = f"{self._PREFIX}{name}"

        # キャッシュキーを生成
        cache_key = f"{logger_name}:{log_dir}"

        # 既に生成済みなら返す
        if cache_key in self._loggers:
            return self._loggers[cache_key]

        # ロガーを生成 (pochi. プレフィックス付き)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        # 既存のハンドラーをクリア（重複防止）
        # pochi. プレフィックス付きなので他ライブラリと衝突しない
        logger.handlers.clear()

        # コンソールハンドラーを追加
        logger.addHandler(create_console_handler(level))

        # ファイルハンドラーを追加（log_dirが指定された場合）
        if log_dir is not None:
            log_path = Path(log_dir) / f"{name.replace('.', '_')}.log"
            logger.addHandler(create_file_handler(log_path, level))

        # 親ロガーへの伝播を無効化
        logger.propagate = False

        # キャッシュに保存
        self._loggers[cache_key] = logger

        return logger
