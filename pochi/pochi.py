"""Pochi main class module.

便利メソッドを集約したファサードクラス.
"""

import logging
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from .config import ConfigLoaderFacade
from .fileops import GlobFileFinder, IFileCopier, IFileFinder, StructurePreservingCopier
from .logging import ILoggerFactory, LoggerFactory
from .timer import ITimerFactory, TimerContext, TimerFactory
from .workspace import IWorkspaceCreator, Workspace, WorkspaceCreator

T = TypeVar("T", bound=BaseModel)


class Pochi:
    """便利メソッドを集約したファサードクラス.

    依存性注入により, テスト時にモックを差し込むことが可能.

    Args:
        workspace_creator: ワークスペース作成の実装.
        logger_factory: ロガー生成の実装.
        timer_factory: タイマー生成の実装.
        config_loader: 設定ローダーの実装.
        file_finder: ファイル検索の実装.
        file_copier: ファイルコピー/移動の実装.
    """

    def __init__(
        self,
        workspace_creator: IWorkspaceCreator | None = None,
        logger_factory: ILoggerFactory | None = None,
        timer_factory: ITimerFactory | None = None,
        config_loader: ConfigLoaderFacade | None = None,
        file_finder: IFileFinder | None = None,
        file_copier: IFileCopier | None = None,
    ) -> None:
        """Pochiを初期化."""
        self._workspace_creator = workspace_creator or WorkspaceCreator()
        self._logger_factory = logger_factory or LoggerFactory()
        self._timer_factory = timer_factory or TimerFactory()
        self._config_loader = config_loader or ConfigLoaderFacade()
        self._file_finder = file_finder or GlobFileFinder()
        self._file_copier = file_copier or StructurePreservingCopier()

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

    def load_config(self, path: str | Path, schema: type[T]) -> T:
        """設定ファイルを読み込み, バリデーションする.

        .py ファイルを読み込み, Pydantic モデルでバリデーションを行う.

        Args:
            path: 設定ファイルのパス.
            schema: バリデーションに使用する Pydantic モデルクラス.

        Returns:
            バリデーション済みの設定オブジェクト.

        Raises:
            FileNotFoundError: ファイルが存在しない場合.
            ValueError: サポートされていない形式, またはバリデーションエラー.

        Examples:
            >>> from pydantic import BaseModel
            >>> class MyConfig(BaseModel):
            ...     epochs: int
            ...     learning_rate: float = 0.001
            >>> pochi = Pochi()
            >>> config = pochi.load_config("config.py", MyConfig)
            >>> print(config.epochs)
            100
        """
        return self._config_loader.load(str(path), schema)

    def find_files(
        self,
        directory: str | Path,
        pattern: str | None = None,
        extensions: list[str] | None = None,
    ) -> list[Path]:
        """ファイルを検索する.

        Args:
            directory: 検索対象のディレクトリ.
            pattern: glob パターン (例: "*.jpg", "**/*.png").
            extensions: 拡張子のリスト (例: [".jpg", ".png"]).

        Returns:
            マッチしたファイルパスのリスト.

        Raises:
            ValueError: pattern と extensions の両方が指定されていない場合.
            FileNotFoundError: ディレクトリが存在しない場合.

        Examples:
            >>> pochi = Pochi()
            >>> files = pochi.find_files("data/", pattern="**/*.jpg")
            >>> files = pochi.find_files("data/", extensions=[".jpg", ".png"])
        """
        return self._file_finder.find(directory, pattern=pattern, extensions=extensions)

    def copy_files(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルをコピーする.

        階層構造を保持してコピーし, メタデータファイルを生成する.

        Args:
            files: コピー対象のファイルリスト.
            dest: コピー先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            コピー先のファイルパスリスト.

        Examples:
            >>> pochi = Pochi()
            >>> files = pochi.find_files("data/", pattern="**/*.jpg")
            >>> pochi.copy_files(files, dest="backup/", base_dir="data/")
            # data/train/cat/001.jpg -> backup/train/cat/001.jpg
        """
        return self._file_copier.copy(files, dest, base_dir=base_dir)

    def move_files(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルを移動する.

        階層構造を保持して移動し, メタデータファイルを生成する.

        Args:
            files: 移動対象のファイルリスト.
            dest: 移動先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            移動先のファイルパスリスト.

        Examples:
            >>> pochi = Pochi()
            >>> files = pochi.find_files("data/", pattern="**/*.jpg")
            >>> pochi.move_files(files, dest="processed/", base_dir="data/")
        """
        return self._file_copier.move(files, dest, base_dir=base_dir)
