"""汎用クラスレジストリの実装."""

from typing import Any, Callable

from .interfaces import IRegistry


class Registry(IRegistry):
    """汎用クラスレジストリ.

    デコレータベースでクラスを登録し, 設定ファイルから動的にインスタンス生成できる.

    Args:
        name: レジストリ名（識別用）.

    Examples:
        >>> registry = Registry("processors")
        >>> @registry.register("blur")
        ... class BlurProcessor:
        ...     def __init__(self, kernel_size: int = 5):
        ...         self.kernel_size = kernel_size
        >>> blur = registry.create("blur", kernel_size=7)
        >>> blur.kernel_size
        7
    """

    def __init__(self, name: str) -> None:
        """Registryを初期化."""
        self._name = name
        self._registry: dict[str, type] = {}

    @property
    def name(self) -> str:
        """レジストリ名を返す."""
        return self._name

    def register(self, name: str) -> Callable[[type], type]:
        """クラス登録デコレータを返す.

        Args:
            name: 登録名.

        Returns:
            デコレータ関数.

        Raises:
            ValueError: 同じ名前が既に登録されている場合.

        Examples:
            >>> registry = Registry("models")
            >>> @registry.register("resnet")
            ... class ResNet:
            ...     pass
        """

        def decorator(cls: type) -> type:
            if name in self._registry:
                raise ValueError(
                    f"'{name}' は既に登録されています: {self._registry[name]}"
                )
            self._registry[name] = cls
            return cls

        return decorator

    def create(self, name: str, **kwargs: Any) -> Any:
        """名前からインスタンスを生成する.

        Args:
            name: 登録名.
            **kwargs: コンストラクタに渡す引数.

        Returns:
            生成されたインスタンス.

        Raises:
            ValueError: 未登録の名前が指定された場合.

        Examples:
            >>> registry = Registry("processors")
            >>> @registry.register("blur")
            ... class Blur:
            ...     def __init__(self, size: int = 3):
            ...         self.size = size
            >>> blur = registry.create("blur", size=5)
        """
        if name not in self._registry:
            available = self.keys()
            raise ValueError(f"未登録: '{name}'. 利用可能: {available}")
        return self._registry[name](**kwargs)

    def keys(self) -> list[str]:
        """登録済みの名前一覧を返す.

        Returns:
            登録名のリスト.

        Examples:
            >>> registry = Registry("models")
            >>> @registry.register("a")
            ... class A: pass
            >>> @registry.register("b")
            ... class B: pass
            >>> registry.keys()
            ['a', 'b']
        """
        return list(self._registry.keys())

    def create_from_config(self, config_list: list[dict[str, Any]]) -> list[Any]:
        """設定リストから複数インスタンスを一括生成する.

        Args:
            config_list: 設定dictのリスト. 各dictには "name" キーが必須.

        Returns:
            生成されたインスタンスのリスト.

        Raises:
            ValueError: 未登録の名前が指定された場合.
            KeyError: "name" キーが存在しない場合.

        Examples:
            >>> registry = Registry("processors")
            >>> @registry.register("blur")
            ... class Blur:
            ...     def __init__(self, size: int = 3):
            ...         self.size = size
            >>> @registry.register("edge")
            ... class Edge:
            ...     def __init__(self, threshold: int = 100):
            ...         self.threshold = threshold
            >>> config = [
            ...     {"name": "blur", "size": 5},
            ...     {"name": "edge", "threshold": 50},
            ... ]
            >>> instances = registry.create_from_config(config)
        """
        result = []
        for step in config_list:
            if "name" not in step:
                raise KeyError("設定には 'name' キーが必要です")
            name = step["name"]
            kwargs = {k: v for k, v in step.items() if k != "name"}
            instance = self.create(name, **kwargs)
            result.append(instance)
        return result

    def __contains__(self, name: str) -> bool:
        """名前が登録済みかチェックする.

        Args:
            name: 登録名.

        Returns:
            登録済みならTrue.
        """
        return name in self._registry

    def __len__(self) -> int:
        """登録済みクラス数を返す."""
        return len(self._registry)
