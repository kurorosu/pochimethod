"""Python設定ファイル (.py) のローダー."""

import importlib.util
from pathlib import Path
from typing import Any

from pochi.config.interfaces import IConfigLoader


class PythonConfigLoader(IConfigLoader):
    """Python設定ファイル (.py) を読み込むローダー.

    .py ファイル内のモジュールレベル変数を dict として取得する.

    Warning:
        このローダーは Python ファイルを実行するため, 信頼できないソースからの
        設定ファイルを読み込むと任意コード実行のリスクがあります.
        自分で作成した設定ファイル, またはコードレビュー済みのファイルのみを
        使用してください.

    Example:
        >>> loader = PythonConfigLoader()
        >>> config = loader.load("config.py")
        >>> print(config["epochs"])
        100
    """

    def load(self, path: str) -> dict[str, Any]:
        """Python設定ファイルを読み込んでdictとして返す.

        Args:
            path: 設定ファイルのパス.

        Returns:
            設定内容のdict. アンダースコアで始まる変数とモジュールは除外.

        Raises:
            FileNotFoundError: ファイルが存在しない場合.
            ValueError: ファイルの読み込みに失敗した場合.
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")

        try:
            # ファイル名からユニークなモジュール名を生成
            module_name = f"pochi_config_{file_path.stem}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec is None or spec.loader is None:
                raise ValueError(f"設定ファイルを読み込めません: {path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # モジュールレベル変数を抽出
            # アンダースコアで始まる変数とモジュールオブジェクトは除外
            config = {
                key: value
                for key, value in vars(module).items()
                if not key.startswith("_") and not isinstance(value, type(module))
            }

            return config

        except SyntaxError as e:
            raise ValueError(f"設定ファイルの構文エラー: {path} - {e}") from e
        except Exception as e:
            raise ValueError(f"設定ファイルの読み込みに失敗: {path} - {e}") from e

    def supports(self, path: str) -> bool:
        """指定されたパスが .py ファイルか判定する.

        Args:
            path: 設定ファイルのパス.

        Returns:
            .py ファイルの場合は True.
        """
        return path.endswith(".py")
