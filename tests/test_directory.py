"""Tests for DirectoryCreator class."""

from pathlib import Path

import pytest

from pochi.directory import DirectoryCreator


class TestDirectoryCreator:
    """DirectoryCreatorクラスのテスト."""

    def test_create_single_directory(self, tmp_path: Path) -> None:
        """単一ディレクトリを作成できることを確認."""
        creator = DirectoryCreator()
        target_dir = tmp_path / "single_dir"

        result = creator.create(target_dir)

        assert result == target_dir
        assert target_dir.exists()
        assert target_dir.is_dir()

    def test_create_nested_directories(self, tmp_path: Path) -> None:
        """ネストしたディレクトリを作成できることを確認."""
        creator = DirectoryCreator()
        target_dir = tmp_path / "a" / "b" / "c"

        result = creator.create(target_dir, parents=True)

        assert result == target_dir
        assert target_dir.exists()

    def test_create_without_parents_raises_error(self, tmp_path: Path) -> None:
        """parents=Falseで親がない場合はエラーになることを確認."""
        creator = DirectoryCreator()
        target_dir = tmp_path / "nonexistent" / "child"

        with pytest.raises(FileNotFoundError):
            creator.create(target_dir, parents=False)

    def test_create_returns_path_object(self, tmp_path: Path) -> None:
        """戻り値がPathオブジェクトであることを確認."""
        creator = DirectoryCreator()
        target_dir = tmp_path / "return_type_test"

        result = creator.create(str(target_dir))

        assert isinstance(result, Path)
