"""設定ローダーのインターフェース定義."""

from abc import ABC, abstractmethod
from typing import Any


class IConfigLoader(ABC):
    """設定ファイルローダーの抽象基底クラス.

    各形式（.py, .json, .yaml等）のローダーはこのインターフェースを実装する.
    """

    @abstractmethod
    def load(self, path: str) -> dict[str, Any]:
        """設定ファイルを読み込んでdictとして返す.

        Args:
            path: 設定ファイルのパス.

        Returns:
            設定内容のdict.

        Raises:
            FileNotFoundError: ファイルが存在しない場合.
            ValueError: ファイルの読み込みに失敗した場合.
        """
        pass

    @abstractmethod
    def supports(self, path: str) -> bool:
        """指定されたパスの形式をサポートするか判定する.

        Args:
            path: 設定ファイルのパス.

        Returns:
            サポートする場合はTrue.
        """
        pass
