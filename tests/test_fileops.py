"""fileops モジュールのテスト."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pochi import Pochi
from pochi.fileops import (
    GlobFileFinder,
    IFileCopier,
    IFileFinder,
    StructurePreservingCopier,
)


class TestGlobFileFinder:
    """GlobFileFinder のテスト."""

    def test_find_with_pattern(self, tmp_path: Path) -> None:
        """glob パターンでファイルを検索できる."""
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        (tmp_path / "file3.jpg").touch()

        finder = GlobFileFinder()
        files = finder.find(tmp_path, pattern="*.txt")

        assert len(files) == 2
        assert all(f.suffix == ".txt" for f in files)

    def test_find_with_recursive_pattern(self, tmp_path: Path) -> None:
        """再帰パターンでファイルを検索できる."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.txt").touch()
        (subdir / "file2.txt").touch()

        finder = GlobFileFinder()
        files = finder.find(tmp_path, pattern="**/*.txt")

        assert len(files) == 2

    def test_find_with_extensions(self, tmp_path: Path) -> None:
        """拡張子リストでファイルを検索できる."""
        (tmp_path / "file1.jpg").touch()
        (tmp_path / "file2.png").touch()
        (tmp_path / "file3.txt").touch()

        finder = GlobFileFinder()
        files = finder.find(tmp_path, extensions=[".jpg", ".png"])

        assert len(files) == 2
        assert all(f.suffix in [".jpg", ".png"] for f in files)

    def test_find_with_extensions_without_dot(self, tmp_path: Path) -> None:
        """ドットなしの拡張子でも検索できる."""
        (tmp_path / "file1.jpg").touch()

        finder = GlobFileFinder()
        files = finder.find(tmp_path, extensions=["jpg"])

        assert len(files) == 1

    def test_find_raises_on_nonexistent_directory(self) -> None:
        """存在しないディレクトリで FileNotFoundError."""
        finder = GlobFileFinder()
        with pytest.raises(FileNotFoundError):
            finder.find("/nonexistent/path", pattern="*.txt")

    def test_find_raises_on_file_path(self, tmp_path: Path) -> None:
        """ファイルパスで ValueError."""
        file_path = tmp_path / "file.txt"
        file_path.touch()

        finder = GlobFileFinder()
        with pytest.raises(ValueError, match="ディレクトリではありません"):
            finder.find(file_path, pattern="*.txt")

    def test_find_raises_without_pattern_or_extensions(self, tmp_path: Path) -> None:
        """pattern と extensions が両方ない場合 ValueError."""
        finder = GlobFileFinder()
        with pytest.raises(ValueError, match="pattern または extensions"):
            finder.find(tmp_path)


class TestStructurePreservingCopier:
    """StructurePreservingCopier のテスト."""

    def test_copy_preserves_structure(self, tmp_path: Path) -> None:
        """階層構造を保持してコピーする."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        (src_dir / "subdir").mkdir(parents=True)
        (src_dir / "subdir" / "file.txt").write_text("content")

        copier = StructurePreservingCopier()
        files = [src_dir / "subdir" / "file.txt"]
        result = copier.copy(files, dest_dir, base_dir=src_dir)

        assert len(result) == 1
        assert (dest_dir / "subdir" / "file.txt").exists()
        assert (dest_dir / "subdir" / "file.txt").read_text() == "content"
        # 元ファイルも存在
        assert (src_dir / "subdir" / "file.txt").exists()

    def test_copy_generates_metadata(self, tmp_path: Path) -> None:
        """メタデータファイルを生成する."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir()
        (src_dir / "file.txt").write_text("content")

        copier = StructurePreservingCopier()
        copier.copy([src_dir / "file.txt"], dest_dir, base_dir=src_dir)

        metadata_path = dest_dir / "_copy_metadata.txt"
        assert metadata_path.exists()
        content = metadata_path.read_text(encoding="utf-8")
        assert "コピー元:" in content
        assert "コピー先:" in content
        assert "実行日時:" in content
        assert "ファイル数: 1" in content

    def test_move_removes_source(self, tmp_path: Path) -> None:
        """移動時に元ファイルが削除される."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir()
        src_file = src_dir / "file.txt"
        src_file.write_text("content")

        copier = StructurePreservingCopier()
        copier.move([src_file], dest_dir, base_dir=src_dir)

        assert not src_file.exists()
        assert (dest_dir / "file.txt").exists()

    def test_move_generates_metadata(self, tmp_path: Path) -> None:
        """移動時にメタデータファイルを生成する."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir()
        (src_dir / "file.txt").write_text("content")

        copier = StructurePreservingCopier()
        copier.move([src_dir / "file.txt"], dest_dir, base_dir=src_dir)

        metadata_path = dest_dir / "_move_metadata.txt"
        assert metadata_path.exists()
        content = metadata_path.read_text(encoding="utf-8")
        assert "移動元:" in content
        assert "移動先:" in content

    def test_copy_without_base_dir(self, tmp_path: Path) -> None:
        """base_dir なしでファイル名のみでコピーする."""
        src_dir = tmp_path / "src" / "subdir"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir(parents=True)
        (src_dir / "file.txt").write_text("content")

        copier = StructurePreservingCopier()
        copier.copy([src_dir / "file.txt"], dest_dir)

        # base_dir がないのでファイル名のみ
        assert (dest_dir / "file.txt").exists()


class TestPochiFileOps:
    """Pochi のファイル操作メソッドのテスト."""

    def test_find_files(self, tmp_path: Path) -> None:
        """Pochi.find_files でファイルを検索できる."""
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()

        pochi = Pochi()
        files = pochi.find_files(tmp_path, pattern="*.txt")

        assert len(files) == 2

    def test_copy_files(self, tmp_path: Path) -> None:
        """Pochi.copy_files でファイルをコピーできる."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir()
        (src_dir / "file.txt").write_text("content")

        pochi = Pochi()
        files = pochi.find_files(src_dir, pattern="*.txt")
        pochi.copy_files(files, dest_dir, base_dir=src_dir)

        assert (dest_dir / "file.txt").exists()

    def test_move_files(self, tmp_path: Path) -> None:
        """Pochi.move_files でファイルを移動できる."""
        src_dir = tmp_path / "src"
        dest_dir = tmp_path / "dest"
        src_dir.mkdir()
        src_file = src_dir / "file.txt"
        src_file.write_text("content")

        pochi = Pochi()
        files = pochi.find_files(src_dir, pattern="*.txt")
        pochi.move_files(files, dest_dir, base_dir=src_dir)

        assert not src_file.exists()
        assert (dest_dir / "file.txt").exists()

    def test_custom_finder_injection(self) -> None:
        """カスタム FileFinder を注入できる."""
        mock_finder = MagicMock(spec=IFileFinder)
        mock_finder.find.return_value = [Path("/mock/file.txt")]

        pochi = Pochi(file_finder=mock_finder)
        result = pochi.find_files("data/", pattern="*.txt")

        assert result == [Path("/mock/file.txt")]
        mock_finder.find.assert_called_once()

    def test_custom_copier_injection(self) -> None:
        """カスタム FileCopier を注入できる."""
        mock_copier = MagicMock(spec=IFileCopier)
        mock_copier.copy.return_value = [Path("/dest/file.txt")]

        pochi = Pochi(file_copier=mock_copier)
        result = pochi.copy_files([Path("/src/file.txt")], "/dest/")

        assert result == [Path("/dest/file.txt")]
        mock_copier.copy.assert_called_once()
