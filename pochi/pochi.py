"""Pochi main class module.

便利メソッドを集約したファサードクラス.
"""

from pathlib import Path

from .workspace import IWorkspaceCreator, Workspace, WorkspaceCreator


class Pochi:
    """便利メソッドを集約したファサードクラス.

    依存性注入により、テスト時にモックを差し込むことが可能.

    Args:
        workspace_creator: ワークスペース作成の実装.
    """

    def __init__(
        self,
        workspace_creator: IWorkspaceCreator | None = None,
    ) -> None:
        """Pochiを初期化."""
        self._workspace_creator = workspace_creator or WorkspaceCreator()

    def create_workspace(
        self,
        base_dir: str | Path | None = None,
        subdirs: list[str] | None = None,
    ) -> Workspace:
        """ワークスペースを作成.

        引数なし: outputs/ のみ作成
        base_dirあり: base_dir/yyyymmdd_xxx/ を作成
        subdirsあり: サブディレクトリも作成

        Args:
            base_dir: ベースディレクトリ. Noneの場合はoutputsのみ作成.
            subdirs: 作成するサブディレクトリ名のリスト.

        Returns:
            作成されたワークスペース情報.

        Examples:
            >>> pochi = Pochi()
            >>> ws = pochi.create_workspace()
            >>> print(ws.root)
            outputs

            >>> ws = pochi.create_workspace("outputs")
            >>> print(ws.root)
            outputs/20241230_001

            >>> ws = pochi.create_workspace("outputs", ["models", "images"])
            >>> print(ws.models)
            outputs/20241230_001/models
        """
        return self._workspace_creator.create(base_dir, subdirs=subdirs)
