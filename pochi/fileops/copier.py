"""ファイルコピー/移動の実装."""

import shutil
from datetime import datetime
from pathlib import Path

from pochi.fileops.interfaces import IFileCopier


class StructurePreservingCopier(IFileCopier):
    """階層構造を保持してコピー/移動する.

    base_dir を基準に相対パスを計算し, dest 以下に同じ構造を再現する.
    メタデータファイル (_copy_metadata.txt, _move_metadata.txt) を自動生成する.

    Example:
        >>> copier = StructurePreservingCopier()
        >>> files = [Path("data/train/cat/001.jpg"), Path("data/train/dog/001.jpg")]
        >>> copier.copy(files, dest="backup/", base_dir="data/")
        # 結果: backup/train/cat/001.jpg, backup/train/dog/001.jpg
    """

    def copy(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルをコピーする.

        Args:
            files: コピー対象のファイルリスト.
            dest: コピー先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            コピー先のファイルパスリスト.
        """
        return self._transfer(files, dest, base_dir, move=False)

    def move(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> list[Path]:
        """ファイルを移動する.

        Args:
            files: 移動対象のファイルリスト.
            dest: 移動先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            移動先のファイルパスリスト.
        """
        return self._transfer(files, dest, base_dir, move=True)

    def _transfer(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None,
        move: bool,
    ) -> list[Path]:
        """ファイルを転送する (コピーまたは移動).

        Args:
            files: 転送対象のファイルリスト.
            dest: 転送先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.
            move: True なら移動, False ならコピー.

        Returns:
            転送先のファイルパスリスト.
        """
        dest_path = Path(dest)
        dest_path.mkdir(parents=True, exist_ok=True)

        base_path = Path(base_dir).resolve() if base_dir else None
        transferred: list[Path] = []

        for src_file in files:
            src_file = src_file.resolve()

            if base_path:
                # 基準ディレクトリからの相対パスを計算
                try:
                    rel_path = src_file.relative_to(base_path)
                except ValueError:
                    # base_dir の外にあるファイルはファイル名のみ使用
                    rel_path = Path(src_file.name)
            else:
                # base_dir がない場合はファイル名のみ
                rel_path = Path(src_file.name)

            dest_file = dest_path / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            if move:
                shutil.move(str(src_file), str(dest_file))
            else:
                shutil.copy2(str(src_file), str(dest_file))

            transferred.append(dest_file)

        # メタデータファイルを生成
        self._write_metadata(
            dest_path,
            base_dir=str(base_path) if base_path else None,
            file_count=len(transferred),
            operation="move" if move else "copy",
        )

        return transferred

    def _write_metadata(
        self,
        dest: Path,
        base_dir: str | None,
        file_count: int,
        operation: str,
    ) -> None:
        """メタデータファイルを生成する.

        Args:
            dest: コピー/移動先ディレクトリ.
            base_dir: 基準ディレクトリ.
            file_count: ファイル数.
            operation: 操作種別 ("copy" or "move").
        """
        metadata_name = f"_{operation}_metadata.txt"
        metadata_path = dest / metadata_name

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source_label = "コピー元" if operation == "copy" else "移動元"
        dest_label = "コピー先" if operation == "copy" else "移動先"

        content = f"""{source_label}: {base_dir or "(指定なし)"}
{dest_label}: {dest}
実行日時: {timestamp}
ファイル数: {file_count}
"""

        metadata_path.write_text(content, encoding="utf-8")

    def mirror_structure(
        self,
        files: list[Path],
        dest: str | Path,
        base_dir: str | Path | None = None,
    ) -> tuple[list[Path], list[Path]]:
        """フォルダ構造のみ作成し, 対応するパスを返す.

        ファイルの中身はコピーせず, 出力先のフォルダ構造だけを作成する.

        Args:
            files: 対象のファイルリスト.
            dest: 出力先ディレクトリ.
            base_dir: 階層構造の基準ディレクトリ.

        Returns:
            (元ファイルパスリスト, 出力先ファイルパスリスト) のタプル.
        """
        dest_path = Path(dest)
        base_path = Path(base_dir).resolve() if base_dir else None

        src_files: list[Path] = []
        dest_files: list[Path] = []

        for src_file in files:
            src_file = src_file.resolve()

            if base_path:
                try:
                    rel_path = src_file.relative_to(base_path)
                except ValueError:
                    rel_path = Path(src_file.name)
            else:
                rel_path = Path(src_file.name)

            dest_file = dest_path / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            src_files.append(src_file)
            dest_files.append(dest_file)

        return src_files, dest_files
