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
        prefix: str | None = None,
    ) -> Workspace:
        """ワークスペースを作成.

        引数なし: outputs/ のみ作成
        base_dirあり: base_dir/yyyymmdd_xxx/ を作成
        prefixあり: base_dir/prefix1, prefix2, ... を作成
        subdirsあり: サブディレクトリも作成

        Args:
            base_dir: ベースディレクトリ. Noneの場合はoutputsのみ作成.
            subdirs: 作成するサブディレクトリ名のリスト.
            prefix: ディレクトリ名のプレフィックス. 指定時は連番形式 (prefix1, prefix2, ...).

        Returns:
            作成されたワークスペース情報.
        """
        # 引数なし: outputsフォルダのみ作成
        if base_dir is None:
            outputs_path = Path("outputs")
            outputs_path.mkdir(parents=True, exist_ok=True)
            return Workspace(root=outputs_path, subdirs=None)

        base_path = Path(base_dir)
        base_path.mkdir(parents=True, exist_ok=True)

        # prefix指定あり: 連番形式 (prefix1, prefix2, ...)
        if prefix is not None:
            workspace_path = self._create_numbered_dir(base_path, prefix)
        else:
            # prefix指定なし: yyyymmdd_xxx形式
            workspace_path = self._create_timestamped_dir(base_path)

        # subdirsあり: サブディレクトリも作成
        if subdirs:
            for subdir in subdirs:
                (workspace_path / subdir).mkdir(exist_ok=True)

        return Workspace(root=workspace_path, subdirs=subdirs)

    def _create_timestamped_dir(self, base_path: Path) -> Path:
        """タイムスタンプ付きディレクトリを作成する.

        Args:
            base_path: ベースディレクトリのパス.

        Returns:
            作成されたディレクトリのパス (yyyymmdd_xxx 形式).
        """
        date_str = get_current_date_str()
        next_index = find_next_index(base_path, date_str)
        workspace_name = format_workspace_name(date_str, next_index)
        workspace_path = base_path / workspace_name
        workspace_path.mkdir(parents=True, exist_ok=True)
        return workspace_path

    def _create_numbered_dir(self, base_path: Path, prefix: str) -> Path:
        """連番ディレクトリを作成する.

        Args:
            base_path: ベースディレクトリのパス.
            prefix: ディレクトリ名のプレフィックス.

        Returns:
            作成されたディレクトリのパス.
        """
        index = 1
        while True:
            target = base_path / f"{prefix}{index}"
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
                return target
            index += 1
