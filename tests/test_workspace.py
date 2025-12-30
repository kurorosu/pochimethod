"""Tests for Workspace functionality."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pochi import Pochi, Workspace
from pochi.workspace import IWorkspaceCreator, WorkspaceCreator
from pochi.workspace.timestamp import (
    find_next_index,
    format_workspace_name,
    get_current_date_str,
)


class TestWorkspace:
    """Workspaceクラスのテスト."""

    def test_root_property(self, tmp_path: Path) -> None:
        """rootプロパティが正しく動作することを確認."""
        ws = Workspace(root=tmp_path, subdirs=["models"])
        assert ws.root == tmp_path

    def test_subdir_access(self, tmp_path: Path) -> None:
        """サブディレクトリへのアクセスが正しく動作することを確認."""
        ws = Workspace(root=tmp_path, subdirs=["models", "images"])
        assert ws.models == tmp_path / "models"
        assert ws.images == tmp_path / "images"

    def test_invalid_subdir_raises_error(self, tmp_path: Path) -> None:
        """存在しないサブディレクトリへのアクセスでエラーになることを確認."""
        ws = Workspace(root=tmp_path, subdirs=["models"])
        with pytest.raises(AttributeError):
            _ = ws.nonexistent

    def test_repr(self, tmp_path: Path) -> None:
        """__repr__が正しく動作することを確認."""
        ws = Workspace(root=tmp_path, subdirs=["models"])
        repr_str = repr(ws)
        assert "Workspace" in repr_str
        assert "models" in repr_str


class TestTimestampUtils:
    """タイムスタンプユーティリティのテスト."""

    def test_get_current_date_str(self) -> None:
        """現在の日付がyyyymmdd形式で取得されることを確認."""
        result = get_current_date_str()
        assert len(result) == 8
        assert result.isdigit()

    def test_format_workspace_name(self) -> None:
        """ワークスペース名が正しくフォーマットされることを確認."""
        assert format_workspace_name("20241230", 1) == "20241230_001"
        assert format_workspace_name("20241230", 99) == "20241230_099"
        assert format_workspace_name("20241230", 100) == "20241230_100"

    def test_find_next_index_empty_dir(self, tmp_path: Path) -> None:
        """空のディレクトリで1が返されることを確認."""
        result = find_next_index(tmp_path, "20241230")
        assert result == 1

    def test_find_next_index_with_existing(self, tmp_path: Path) -> None:
        """既存のディレクトリがある場合に次のインデックスが返されることを確認."""
        (tmp_path / "20241230_001").mkdir()
        (tmp_path / "20241230_002").mkdir()
        result = find_next_index(tmp_path, "20241230")
        assert result == 3

    def test_find_next_index_nonexistent_dir(self, tmp_path: Path) -> None:
        """存在しないディレクトリで1が返されることを確認."""
        result = find_next_index(tmp_path / "nonexistent", "20241230")
        assert result == 1


class TestWorkspaceCreator:
    """WorkspaceCreatorクラスのテスト."""

    def test_create_without_args(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """引数なしでoutputsフォルダのみ作成されることを確認."""
        monkeypatch.chdir(tmp_path)
        creator = WorkspaceCreator()

        ws = creator.create()

        assert ws.root == Path("outputs")
        assert (tmp_path / "outputs").exists()

    @patch("pochi.workspace.creator.get_current_date_str")
    def test_create_with_base_dir(self, mock_date: MagicMock, tmp_path: Path) -> None:
        """base_dirありでyyyymmdd_xxxが作成されることを確認."""
        mock_date.return_value = "20241230"
        creator = WorkspaceCreator()

        ws = creator.create(tmp_path)

        assert ws.root == tmp_path / "20241230_001"
        assert ws.root.exists()

    @patch("pochi.workspace.creator.get_current_date_str")
    def test_create_with_subdirs(self, mock_date: MagicMock, tmp_path: Path) -> None:
        """subdirsありでサブフォルダも作成されることを確認."""
        mock_date.return_value = "20241230"
        creator = WorkspaceCreator()

        ws = creator.create(tmp_path, subdirs=["models", "images"])

        assert ws.root == tmp_path / "20241230_001"
        assert (ws.root / "models").exists()
        assert (ws.root / "images").exists()
        assert ws.models == tmp_path / "20241230_001" / "models"
        assert ws.images == tmp_path / "20241230_001" / "images"

    @patch("pochi.workspace.creator.get_current_date_str")
    def test_create_increments_index(
        self, mock_date: MagicMock, tmp_path: Path
    ) -> None:
        """インデックスが正しくインクリメントされることを確認."""
        mock_date.return_value = "20241230"
        creator = WorkspaceCreator()

        ws1 = creator.create(tmp_path)
        ws2 = creator.create(tmp_path)

        assert ws1.root.name == "20241230_001"
        assert ws2.root.name == "20241230_002"


class TestPochiCreateWorkspace:
    """Pochi.create_workspaceメソッドのテスト."""

    def test_create_workspace_without_args(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """引数なしでoutputsフォルダのみ作成されることを確認."""
        monkeypatch.chdir(tmp_path)
        pochi = Pochi()

        ws = pochi.create_workspace()

        assert ws.root == Path("outputs")
        assert (tmp_path / "outputs").exists()

    @patch("pochi.workspace.creator.get_current_date_str")
    def test_create_workspace_with_base_dir(
        self, mock_date: MagicMock, tmp_path: Path
    ) -> None:
        """base_dirありでワークスペースが作成されることを確認."""
        mock_date.return_value = "20241230"
        pochi = Pochi()

        ws = pochi.create_workspace(tmp_path)

        assert ws.root == tmp_path / "20241230_001"

    @patch("pochi.workspace.creator.get_current_date_str")
    def test_create_workspace_with_subdirs(
        self, mock_date: MagicMock, tmp_path: Path
    ) -> None:
        """subdirsありでワークスペースとサブフォルダが作成されることを確認."""
        mock_date.return_value = "20241230"
        pochi = Pochi()

        ws = pochi.create_workspace(tmp_path, subdirs=["models", "logs"])

        assert ws.root == tmp_path / "20241230_001"
        assert ws.models == tmp_path / "20241230_001" / "models"
        assert ws.logs == tmp_path / "20241230_001" / "logs"

    def test_create_workspace_with_mock_creator(self) -> None:
        """カスタムWorkspaceCreatorを注入できることを確認."""
        mock_creator = MagicMock(spec=IWorkspaceCreator)
        expected_ws = Workspace(root=Path("/mock"), subdirs=["test"])
        mock_creator.create.return_value = expected_ws

        pochi = Pochi(workspace_creator=mock_creator)
        result = pochi.create_workspace("outputs", subdirs=["test"])

        assert result == expected_ws
        mock_creator.create.assert_called_once_with("outputs", subdirs=["test"])
