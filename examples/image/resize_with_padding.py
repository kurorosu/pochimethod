"""アスペクト比を保持した画像リサイズのサンプル.

フォルダ構造を維持しながら, 画像を指定サイズにパディングリサイズします.
CNN学習用データセットの前処理に便利です.

使い方:
    uv run python examples/image/resize_with_padding.py

入力フォルダ構造の例:
    examples/image/data/train/
    ├── cat/
    │   ├── 001.jpg
    │   └── 002.jpg
    └── dog/
        ├── 001.jpg
        └── 002.jpg

出力フォルダ構造:
    examples/image/data_resized/train/
    ├── cat/
    │   ├── 001.jpg   (640x640, パディング付き)
    │   └── 002.jpg
    └── dog/
        ├── 001.jpg
        └── 002.jpg
"""

from pathlib import Path

from pochi import Pochi

# ===== 設定 =====
EXAMPLE_DIR = Path(__file__).parent
SRC_DIR = EXAMPLE_DIR / "data" / "train"
DST_DIR = EXAMPLE_DIR / "data_resized" / "train"
TARGET_SIZE = 640  # 正方形の場合は int, 矩形の場合は (width, height)
EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

# ===== 実行 =====
pochi = Pochi()

# 1. 画像ファイルを検索
files = pochi.find_files(SRC_DIR, extensions=EXTENSIONS)
print(f"検出した画像: {len(files)} 枚")

# 2. フォルダ構造をミラーリング (ファイルはコピーしない)
src_files, dst_files = pochi.mirror_structure(files, dest=DST_DIR, base_dir=SRC_DIR)

# 3. アスペクト比を保持してリサイズ
for src, dst in zip(src_files, dst_files):
    pochi.resize_image(src, dst, size=TARGET_SIZE, mode="long", padding_color=(0, 0, 0))
    print(f"  {src} -> {dst}")

print(f"完了: {len(src_files)} 枚をリサイズしました")
