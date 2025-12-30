"""Workspace interfaces module.

ワークスペース関連のインターフェース定義.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Workspace


class IWorkspaceCreator(ABC):
    """ワークスペース作成のインターフェース."""

    @abstractmethod
    def create(
        self,
        base_dir: str | Path | None = None,
        subdirs: list[str] | None = None,
    ) -> "Workspace":
        """ワークスペースを作成.

        Args:
            base_dir: ベースディレクトリ. Noneの場合はoutputsのみ作成.
            subdirs: 作成するサブディレクトリ名のリスト.

        Returns:
            作成されたワークスペース情報.
        """
        ...
