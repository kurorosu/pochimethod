"""設定ローダーのファサード."""

from typing import Any, TypeVar

from pydantic import BaseModel

from pochi.config.interfaces import IConfigLoader
from pochi.config.json_loader import JsonConfigLoader
from pochi.config.python_loader import PythonConfigLoader
from pochi.config.yaml_loader import YamlConfigLoader

T = TypeVar("T", bound=BaseModel)


class ConfigLoaderFacade:
    """設定ファイルローダーのファサード.

    複数の形式のローダーを管理し, 適切なローダーを選択して読み込む.
    Pydantic モデルによる厳格なバリデーション (strict=True) を行う.
    型の自動変換は行わず, 型が一致しない場合はエラーになる.

    Example:
        >>> from pydantic import BaseModel
        >>> class MyConfig(BaseModel):
        ...     epochs: int
        ...     learning_rate: float
        >>> facade = ConfigLoaderFacade()
        >>> config = facade.load("config.py", MyConfig)
        >>> print(config.epochs)
        100
    """

    def __init__(self, loaders: list[IConfigLoader] | None = None) -> None:
        """初期化する.

        Args:
            loaders: 使用するローダーのリスト. None の場合はデフォルトのローダーを使用.
        """
        self._loaders = loaders or [
            PythonConfigLoader(),
            JsonConfigLoader(),
            YamlConfigLoader(),
        ]

    def load(self, path: str, schema: type[T]) -> T:
        """設定ファイルを読み込み, Pydantic モデルでバリデーションする.

        Args:
            path: 設定ファイルのパス.
            schema: バリデーションに使用する Pydantic モデルクラス.

        Returns:
            バリデーション済みの設定オブジェクト.

        Raises:
            ValueError: サポートされていない形式の場合, またはバリデーションエラー.
            FileNotFoundError: ファイルが存在しない場合.
        """
        for loader in self._loaders:
            if loader.supports(path):
                data = loader.load(path)
                # strict=True で型の自動変換を無効化
                result: T = schema.model_validate(data, strict=True)
                return result

        supported = [type(loader).__name__ for loader in self._loaders]
        raise ValueError(
            f"サポートされていない設定ファイル形式: {path} "
            f"(対応ローダー: {supported})"
        )

    def load_dict(self, path: str) -> dict[str, Any]:
        """設定ファイルを読み込み, dict として返す.

        バリデーションなしで dict を取得したい場合に使用.

        Args:
            path: 設定ファイルのパス.

        Returns:
            設定内容の dict.

        Raises:
            ValueError: サポートされていない形式の場合.
            FileNotFoundError: ファイルが存在しない場合.
        """
        for loader in self._loaders:
            if loader.supports(path):
                return loader.load(path)

        supported = [type(loader).__name__ for loader in self._loaders]
        raise ValueError(
            f"サポートされていない設定ファイル形式: {path} "
            f"(対応ローダー: {supported})"
        )

    def register_loader(self, loader: IConfigLoader) -> None:
        """ローダーを追加登録する.

        Args:
            loader: 追加するローダー.
        """
        self._loaders.append(loader)
