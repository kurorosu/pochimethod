"""Tests for Pochi class."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pochi import IDirectoryCreator, Pochi


class TestPochi:
    """Pochiクラスのテスト."""

    def test_mkdir_creates_directory(self, tmp_path: Path) -> None:
        """mkdirがディレクトリを作成することを確認."""
        pochi = Pochi()
        target_dir = tmp_path / "test_dir"

        result = pochi.mkdir(target_dir)

        assert result == target_dir
        assert target_dir.exists()
        assert target_dir.is_dir()

    def test_mkdir_creates_nested_directory(self, tmp_path: Path) -> None:
        """mkdirがネストしたディレクトリを作成することを確認."""
        pochi = Pochi()
        target_dir = tmp_path / "parent" / "child" / "grandchild"

        result = pochi.mkdir(target_dir)

        assert result == target_dir
        assert target_dir.exists()

    def test_mkdir_returns_path_when_already_exists(self, tmp_path: Path) -> None:
        """既存ディレクトリの場合もパスを返すことを確認."""
        pochi = Pochi()
        target_dir = tmp_path / "existing_dir"
        target_dir.mkdir()

        result = pochi.mkdir(target_dir)

        assert result == target_dir

    def test_mkdir_accepts_string_path(self, tmp_path: Path) -> None:
        """文字列パスを受け付けることを確認."""
        pochi = Pochi()
        target_dir = tmp_path / "string_path_dir"

        result = pochi.mkdir(str(target_dir))

        assert result == target_dir
        assert target_dir.exists()

    def test_mkdir_with_custom_directory_creator(self) -> None:
        """カスタムDirectoryCreatorを注入できることを確認."""
        mock_creator = MagicMock(spec=IDirectoryCreator)
        expected_path = Path("/mock/path")
        mock_creator.create.return_value = expected_path

        pochi = Pochi(directory_creator=mock_creator)
        result = pochi.mkdir("/some/path")

        assert result == expected_path
        mock_creator.create.assert_called_once_with("/some/path", parents=True)
