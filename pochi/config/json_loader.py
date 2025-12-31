"""JSON設定ファイル (.json) のローダー."""

import json
from pathlib import Path
from typing import Any

from pochi.config.interfaces import IConfigLoader


class JsonConfigLoader(IConfigLoader):
    """JSON設定ファイル (.json) を読み込むローダー.

    .json ファイルを読み込んで dict として返す.

    Example:
        >>> loader = JsonConfigLoader()
        >>> config = loader.load("config.json")
        >>> print(config["epochs"])
        100
    """

    def load(self, path: str) -> dict[str, Any]:
        """JSON設定ファイルを読み込んでdictとして返す.

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
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError(
                    f"設定ファイルのルートはオブジェクトである必要があります: {path}"
                )

            return data

        except json.JSONDecodeError as e:
            raise ValueError(f"JSONの構文エラー: {path} - {e}") from e
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"設定ファイルの読み込みに失敗: {path} - {e}") from e

    def supports(self, path: str) -> bool:
        """指定されたパスが .json ファイルか判定する.

        Args:
            path: 設定ファイルのパス.

        Returns:
            .json ファイルの場合は True.
        """
        return path.endswith(".json")
