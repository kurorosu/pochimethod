"""Timestamp utilities module.

タイムスタンプ関連のユーティリティ.
"""

from datetime import datetime
from pathlib import Path


def get_current_date_str() -> str:
    """現在の日付を yyyymmdd 形式で取得.

    Returns:
        yyyymmdd 形式の日付文字列.
    """
    return datetime.now().strftime("%Y%m%d")


def find_next_index(base_dir: Path, date_str: str) -> int:
    """指定された日付の次のインデックスを取得.

    Args:
        base_dir: ベースディレクトリ.
        date_str: 日付文字列 (yyyymmdd).

    Returns:
        次のインデックス番号 (1から開始).
    """
    if not base_dir.exists():
        return 1

    existing_indices: list[int] = []
    for path in base_dir.iterdir():
        if path.is_dir() and path.name.startswith(date_str + "_"):
            try:
                index_str = path.name.split("_")[1]
                existing_indices.append(int(index_str))
            except (IndexError, ValueError):
                continue

    if not existing_indices:
        return 1

    return max(existing_indices) + 1


def format_workspace_name(date_str: str, index: int) -> str:
    """ワークスペース名をフォーマット.

    Args:
        date_str: 日付文字列 (yyyymmdd).
        index: インデックス番号.

    Returns:
        yyyymmdd_xxx 形式のワークスペース名.
    """
    return f"{date_str}_{index:03d}"
