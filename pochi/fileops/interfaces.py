"""ファイル操作のインターフェース定義."""

from abc import ABC, abstractmethod
from pathlib import Path


class IFileFinder(ABC):
    """ファイル検索のインターフェース."""

    @abstractmethod
    def find(
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
        """
        pass


class IFileCopier(ABC):
    """ファイルコピー/移動のインターフェース."""

    @abstractmethod
    def copy(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルをコピーする.

        Args:
            files: コピー対象のファイルリスト.
            dest: コピー先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            コピー先のファイルパスリスト.
        """
        pass

    @abstractmethod
    def move(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルを移動する.

        Args:
            files: 移動対象のファイルリスト.
            dest: 移動先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            移動先のファイルパスリスト.
        """
        pass
