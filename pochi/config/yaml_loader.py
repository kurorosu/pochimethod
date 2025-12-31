"""YAML設定ファイル (.yaml, .yml) のローダー."""

from pathlib import Path
from typing import Any

import yaml

from pochi.config.interfaces import IConfigLoader


class YamlConfigLoader(IConfigLoader):
    """YAML設定ファイル (.yaml, .yml) を読み込むローダー.

    .yaml または .yml ファイルを読み込んで dict として返す.

    Example:
        >>> loader = YamlConfigLoader()
        >>> config = loader.load("config.yaml")
        >>> print(config["epochs"])
        100
    """

    def load(self, path: str) -> dict[str, Any]:
        """YAML設定ファイルを読み込んでdictとして返す.

        Args:
            path: 設定ファイルのパス.

        Returns:
            設定内容のdict.

        Raises:
            FileNotFoundError: ファイルが存在しない場合.
            ValueError: ファイルの読み込みに失敗した場合.
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")

        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data is None:
                return {}

            if not isinstance(data, dict):
                raise ValueError(
                    f"設定ファイルのルートはオブジェクトである必要があります: {path}"
                )

            return data

        except yaml.YAMLError as e:
            raise ValueError(f"YAMLの構文エラー: {path} - {e}") from e
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"設定ファイルの読み込みに失敗: {path} - {e}") from e

    def supports(self, path: str) -> bool:
        """指定されたパスが .yaml または .yml ファイルか判定する.

        Args:
            path: 設定ファイルのパス.

        Returns:
            .yaml または .yml ファイルの場合は True.
        """
        return path.endswith(".yaml") or path.endswith(".yml")
