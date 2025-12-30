"""Workspace models module.

ワークスペースの戻り値モデル.
"""

from pathlib import Path


class Workspace:
    """ワークスペース情報を保持するクラス.

    動的にサブディレクトリへの属性アクセスを提供.

    Args:
        root: ワークスペースのルートパス.
        subdirs: サブディレクトリ名のリスト.
    """

    def __init__(self, root: Path, subdirs: list[str] | None = None) -> None:
        """Workspaceを初期化."""
        self._root = root
        self._subdirs: dict[str, Path] = {}

        if subdirs:
            for name in subdirs:
                self._subdirs[name] = root / name

    @property
    def root(self) -> Path:
        """ワークスペースのルートパスを取得."""
        return self._root

    def __getattr__(self, name: str) -> Path:
        """サブディレクトリへの動的アクセス.

        Args:
            name: サブディレクトリ名.

        Returns:
            サブディレクトリのPath.

        Raises:
            AttributeError: 存在しないサブディレクトリにアクセスした場合.
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        if name in self._subdirs:
            return self._subdirs[name]

        raise AttributeError(
            f"'{type(self).__name__}' has no subdir '{name}'. "
            f"Available: {list(self._subdirs.keys())}"
        )

    def __repr__(self) -> str:
        """文字列表現を返す."""
        return f"Workspace(root={self._root}, subdirs={list(self._subdirs.keys())})"
