"""Pochi main class module.

便利メソッドを集約したファサードクラス.
"""

import logging
from pathlib import Path

from .logging import ILoggerFactory, LoggerFactory
from .timer import ITimerFactory, TimerContext, TimerFactory
from .workspace import IWorkspaceCreator, Workspace, WorkspaceCreator


class Pochi:
    """便利メソッドを集約したファサードクラス.

    依存性注入により、テスト時にモックを差し込むことが可能.

    Args:
        workspace_creator: ワークスペース作成の実装.
        logger_factory: ロガー生成の実装.
        timer_factory: タイマー生成の実装.
    """

    def __init__(
        self,
        workspace_creator: IWorkspaceCreator | None = None,
        logger_factory: ILoggerFactory | None = None,
        timer_factory: ITimerFactory | None = None,
    ) -> None:
        """Pochiを初期化."""
        self._workspace_creator = workspace_creator or WorkspaceCreator()
        self._logger_factory = logger_factory or LoggerFactory()
        self._timer_factory = timer_factory or TimerFactory()

    def create_workspace(
        self,
        base_dir: str | Path | None = None,
        subdirs: list[str] | None = None,
    ) -> Workspace:
        """ワークスペースを作成.

        引数なし: outputs/ のみ作成
        base_dirあり: base_dir/yyyymmdd_xxx/ を作成
        subdirsあり: サブディレクトリも作成

        Args:
            base_dir: ベースディレクトリ. Noneの場合はoutputsのみ作成.
            subdirs: 作成するサブディレクトリ名のリスト.

        Returns:
            作成されたワークスペース情報.

        Examples:
            >>> pochi = Pochi()
            >>> ws = pochi.create_workspace()
            >>> print(ws.root)
            outputs

            >>> ws = pochi.create_workspace("outputs")
            >>> print(ws.root)
            outputs/20241230_001

            >>> ws = pochi.create_workspace("outputs", ["models", "images"])
            >>> print(ws.models)
            outputs/20241230_001/models
        """
        return self._workspace_creator.create(base_dir, subdirs=subdirs)

    def get_logger(
        self,
        name: str,
        log_dir: str | Path | None = None,
        level: int = logging.INFO,
    ) -> logging.Logger:
        """ロガーを取得.

        コンソール出力（色付き）とファイル出力（プレーン）を提供.

        Args:
            name: ロガー名. 通常は __name__ を指定.
            log_dir: ログファイル出力先ディレクトリ. Noneの場合はコンソールのみ.
            level: ログレベル.

        Returns:
            設定済みのロガー.

        Examples:
            >>> pochi = Pochi()
            >>> logger = pochi.get_logger(__name__)
            >>> logger.info("コンソールのみ出力")

            >>> ws = pochi.create_workspace("outputs", ["logs"])
            >>> logger = pochi.get_logger(__name__, ws.logs)
            >>> logger.info("コンソール + ファイル出力")
        """
        return self._logger_factory.create(name, log_dir=log_dir, level=level)

    def timer(
        self,
        name: str,
        logger: logging.Logger | None = None,
    ) -> TimerContext:
        """タイマーコンテキストマネージャーを取得.

        処理時間を計測し、終了時にログ出力.

        Args:
            name: タイマー名（ログ出力時に使用）.
            logger: ログ出力先. Noneの場合はprint出力.

        Returns:
            コンテキストマネージャーとして使用可能なタイマー.

        Examples:
            >>> pochi = Pochi()
            >>> with pochi.timer("処理A"):
            ...     do_something()
            処理A: 1.234s

            >>> logger = pochi.get_logger(__name__)
            >>> with pochi.timer("処理B", logger):
            ...     do_something()
            # ロガー経由で出力
        """
        return self._timer_factory.create(name, logger=logger)
