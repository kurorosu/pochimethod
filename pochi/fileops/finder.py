"""ファイル検索の実装."""

from pathlib import Path

from pochi.fileops.interfaces import IFileFinder


class GlobFileFinder(IFileFinder):
    """glob パターンによるファイル検索.

    Example:
        >>> finder = GlobFileFinder()
        >>> files = finder.find("data/", pattern="**/*.jpg")
        >>> files = finder.find("data/", extensions=[".jpg", ".png"])
    """

    def find(
        self,
        directory: str | Path,
        pattern: str | None = None,
        extensions: list[str] | None = None,
    ) -> list[Path]:
        """ファイルを検索する.

        Args:
            directory: 検索対象のディレクトリ.
            pattern: glob パターン (例: "*.jpg", "**/*.png").
            extensions: 拡張子のリスト (例: [".jpg", ".png"]).

        Returns:
            マッチしたファイルパスのリスト.

        Raises:
            ValueError: pattern と extensions の両方が指定されていない場合.
            FileNotFoundError: ディレクトリが存在しない場合.
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            raise FileNotFoundError(f"ディレクトリが存在しません: {directory}")

        if not dir_path.is_dir():
            raise ValueError(f"ディレクトリではありません: {directory}")

        if pattern is None and extensions is None:
            raise ValueError("pattern または extensions のいずれかを指定してください")

        if pattern is not None:
            # glob パターンで検索
            files = [p for p in dir_path.glob(pattern) if p.is_file()]
        else:
            # 拡張子でフィルタ (再帰検索)
            files = []
            for ext in extensions or []:
                # 拡張子が . で始まっていなければ追加
                if not ext.startswith("."):
                    ext = f".{ext}"
                files.extend(p for p in dir_path.rglob(f"*{ext}") if p.is_file())

        # ソートして返す
        return sorted(files)
