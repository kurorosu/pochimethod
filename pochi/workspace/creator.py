"""Workspace creator module.

ワークスペース作成の実装.
"""

from pathlib import Path

from .interfaces import IWorkspaceCreator
from .models import Workspace
from .timestamp import find_next_index, format_workspace_name, get_current_date_str


class WorkspaceCreator(IWorkspaceCreator):
    """ワークスペース作成の実装クラス."""

    def create(
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
        """
        # 引数なし: outputsフォルダのみ作成
        if base_dir is None:
            outputs_path = Path("outputs")
            outputs_path.mkdir(parents=True, exist_ok=True)
            return Workspace(root=outputs_path, subdirs=None)

        # base_dirあり: yyyymmdd_xxx形式のワークスペースを作成
        base_path = Path(base_dir)
        base_path.mkdir(parents=True, exist_ok=True)

        date_str = get_current_date_str()
        next_index = find_next_index(base_path, date_str)
        workspace_name = format_workspace_name(date_str, next_index)

        workspace_path = base_path / workspace_name
        workspace_path.mkdir(parents=True, exist_ok=True)

        # subdirsあり: サブディレクトリも作成
        if subdirs:
            for subdir in subdirs:
                (workspace_path / subdir).mkdir(exist_ok=True)

        return Workspace(root=workspace_path, subdirs=subdirs)
