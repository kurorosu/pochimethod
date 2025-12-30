"""Directory creation module.

ディレクトリ作成のインターフェースと実装.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class IDirectoryCreator(ABC):
    """ディレクトリ作成のインターフェース."""

    @abstractmethod
    def create(self, path: str | Path, parents: bool = True) -> Path:
        """ディレクトリを作成し、作成したパスを返す.

        Args:
            path: 作成するディレクトリのパス.
            parents: 親ディレクトリも作成するかどうか.

        Returns:
            作成されたディレクトリのPath.
        """
        ...


class DirectoryCreator(IDirectoryCreator):
    """ディレクトリ作成の実装クラス."""

    def create(self, path: str | Path, parents: bool = True) -> Path:
        """ディレクトリを作成し、作成したパスを返す.

        Args:
            path: 作成するディレクトリのパス.
            parents: 親ディレクトリも作成するかどうか.

        Returns:
            作成されたディレクトリのPath.
        """
        dir_path = Path(path)
        dir_path.mkdir(parents=parents, exist_ok=True)
        return dir_path
