"""アスペクト比保持リサイズ機能."""

from pathlib import Path

from PIL import Image


def resize_with_padding(
    src: str | Path,
    dst: str | Path,
    size: int | tuple[int, int],
    mode: str = "long",
    padding_color: tuple[int, int, int] = (0, 0, 0),
) -> Path:
    """アスペクト比を保持して画像をリサイズし, 足りない部分をパディングする.

    Args:
        src: 入力画像パス.
        dst: 出力画像パス.
        size: 出力サイズ. int なら正方形, tuple なら (width, height).
        mode: リサイズ基準.
            - "long": 長辺を size に合わせる（画像全体が収まる）.
            - "short": 短辺を size に合わせる（はみ出し部分はクロップ）.
        padding_color: パディング色 (R, G, B). デフォルトは黒.

    Returns:
        出力画像パス.

    Raises:
        FileNotFoundError: 入力画像が存在しない場合.
        ValueError: 無効な mode が指定された場合.

    Examples:
        >>> resize_with_padding("input.jpg", "output.jpg", 224)
        # 224x224 の正方形にリサイズ + パディング

        >>> resize_with_padding("input.jpg", "output.jpg", (640, 480))
        # 640x480 にリサイズ + パディング
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if not src_path.exists():
        raise FileNotFoundError(f"入力画像が見つかりません: {src_path}")

    if mode not in ("long", "short"):
        raise ValueError(
            f"無効な mode: {mode}. 'long' または 'short' を指定してください"
        )

    # 出力サイズを決定
    if isinstance(size, int):
        target_w, target_h = size, size
    else:
        target_w, target_h = size

    # 画像を読み込み
    img = Image.open(src_path)

    # RGBAの場合はRGBに変換
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, padding_color)
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    orig_w, orig_h = img.size

    # アスペクト比を保持してリサイズ
    if mode == "long":
        # 長辺を基準: 画像全体が収まるようにする
        ratio = min(target_w / orig_w, target_h / orig_h)
    else:
        # 短辺を基準: 短辺を合わせる（はみ出しはクロップ）
        ratio = max(target_w / orig_w, target_h / orig_h)

    new_w = int(orig_w * ratio)
    new_h = int(orig_h * ratio)
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)

    # 結果画像を作成
    result = Image.new("RGB", (target_w, target_h), padding_color)

    if mode == "long":
        # 中央に配置
        paste_x = (target_w - new_w) // 2
        paste_y = (target_h - new_h) // 2
        result.paste(img_resized, (paste_x, paste_y))
    else:
        # 中央からクロップ
        crop_x = (new_w - target_w) // 2
        crop_y = (new_h - target_h) // 2
        img_cropped = img_resized.crop(
            (crop_x, crop_y, crop_x + target_w, crop_y + target_h)
        )
        result.paste(img_cropped, (0, 0))

    # 出力ディレクトリを作成
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存
    result.save(dst_path)

    return dst_path
