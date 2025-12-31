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

    @abstractmethod
    def mirror_structure(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> tuple[list[Path], list[Path]]:
        """フォルダ構造のみ作成し, 対応するパスを返す.

        ファイルの中身はコピーせず, 出力先のフォルダ構造だけを作成する.
        処理後のファイルを元と同じ構造で保存したい場合に便利.

        Args:
            files: 対象のファイルリスト.
            dest: 出力先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            (元ファイルパスリスト, 出力先ファイルパスリスト) のタプル.
        """
        pass
