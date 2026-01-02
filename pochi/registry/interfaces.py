"""レジストリのインターフェース定義."""

from abc import ABC, abstractmethod
from typing import Any, Callable


class IRegistry(ABC):
    """クラスレジストリの抽象基底クラス.

    デコレータベースでクラスを登録し, 名前から動的にインスタンス生成する.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """レジストリ名を返す."""
        pass

    @abstractmethod
    def __contains__(self, name: str) -> bool:
        """名前が登録済みかチェックする.

        Args:
            name: 登録名.

        Returns:
            登録済みならTrue.
        """
        pass

    @abstractmethod
    def register(self, name: str) -> Callable[[type], type]:
        """クラス登録デコレータを返す.

        Args:
            name: 登録名.

        Returns:
            デコレータ関数.
        """
        pass

    @abstractmethod
    def create(self, name: str, **kwargs: Any) -> Any:
        """名前からインスタンスを生成する.

        Args:
            name: 登録名.
            **kwargs: コンストラクタに渡す引数.

        Returns:
            生成されたインスタンス.

        Raises:
            ValueError: 未登録の名前が指定された場合.
        """
        pass

    @abstractmethod
    def keys(self) -> list[str]:
        """登録済みの名前一覧を返す.

        Returns:
            登録名のリスト.
        """
        pass

    @abstractmethod
    def create_from_config(self, config_list: "list[dict[str, Any]]") -> "list[Any]":
        """設定リストから複数インスタンスを一括生成する.

        Args:
            config_list: 設定dictのリスト. 各dictには "name" キーが必須.

        Returns:
            生成されたインスタンスのリスト.

        Raises:
            ValueError: 未登録の名前が指定された場合.
            KeyError: "name" キーが存在しない場合.
        """
        pass
