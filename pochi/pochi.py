"""Pochi main class module.

便利メソッドを集約したファサードクラス.
"""

from pathlib import Path

from .directory import DirectoryCreator, IDirectoryCreator


class Pochi:
    """便利メソッドを集約したファサードクラス.

    依存性注入により、テスト時にモックを差し込むことが可能.

    Args:
        directory_creator: ディレクトリ作成の実装.
    """

    def __init__(
        self,
        directory_creator: IDirectoryCreator | None = None,
    ) -> None:
        """Pochiを初期化."""
        self._directory_creator = directory_creator or DirectoryCreator()

    def mkdir(self, path: str | Path, parents: bool = True) -> Path:
        """ディレクトリを作成し、作成したパスを返す.

        Args:
            path: 作成するディレクトリのパス.
            parents: 親ディレクトリも作成するかどうか.

        Returns:
            作成されたディレクトリのPath.

        Examples:
            >>> pochi = Pochi()
            >>> created_path = pochi.mkdir("output/data")
            >>> print(created_path)
            output/data
        """
        return self._directory_creator.create(path, parents=parents)
