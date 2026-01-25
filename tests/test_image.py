"""Tests for Image resizing functionality."""

from pathlib import Path

import pytest
from PIL import Image

from pochi import Pochi
from pochi.image import resize_with_padding


class TestResizeWithPadding:
    """resize_with_padding関数のテスト."""

    def test_resize_square_image_to_square(self, tmp_path: Path) -> None:
        """正方形画像を正方形にリサイズできることを確認."""
        # 100x100 の画像を作成
        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (100, 100), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "output.jpg"
        result = resize_with_padding(src, dst, size=50)

        assert result == dst
        assert dst.exists()

        output_img = Image.open(dst)
        assert output_img.size == (50, 50)

    def test_resize_horizontal_image_with_padding(self, tmp_path: Path) -> None:
        """横長画像をパディング付きでリサイズできることを確認."""
        # 200x100 の横長画像を作成（PNGで圧縮誤差を回避）
        src = tmp_path / "horizontal.png"
        img = Image.new("RGB", (200, 100), (0, 255, 0))
        img.save(src)

        dst = tmp_path / "output.png"
        result = resize_with_padding(src, dst, size=100)

        assert result == dst
        output_img = Image.open(dst)
        assert output_img.size == (100, 100)

        # 上下にパディングがあることを確認（中央ピクセルは緑）
        center_pixel = output_img.getpixel((50, 50))
        assert center_pixel == (0, 255, 0)

        # 上端はパディング（黒）
        top_pixel = output_img.getpixel((50, 0))
        assert top_pixel == (0, 0, 0)

    def test_resize_vertical_image_with_padding(self, tmp_path: Path) -> None:
        """縦長画像をパディング付きでリサイズできることを確認."""
        # 100x200 の縦長画像を作成（PNGで圧縮誤差を回避）
        src = tmp_path / "vertical.png"
        img = Image.new("RGB", (100, 200), (0, 0, 255))
        img.save(src)

        dst = tmp_path / "output.png"
        result = resize_with_padding(src, dst, size=100)

        assert result == dst
        output_img = Image.open(dst)
        assert output_img.size == (100, 100)

        # 左右にパディングがあることを確認（中央ピクセルは青）
        center_pixel = output_img.getpixel((50, 50))
        assert center_pixel == (0, 0, 255)

        # 左端はパディング（黒）
        left_pixel = output_img.getpixel((0, 50))
        assert left_pixel == (0, 0, 0)

    def test_resize_with_custom_padding_color(self, tmp_path: Path) -> None:
        """カスタムパディング色を使用できることを確認."""
        # 200x100 の横長画像を作成
        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (200, 100), (255, 255, 255))
        img.save(src)

        dst = tmp_path / "output.jpg"
        resize_with_padding(src, dst, size=100, padding_color=(128, 128, 128))

        output_img = Image.open(dst)
        # 上端はパディング（グレー）
        top_pixel = output_img.getpixel((50, 0))
        assert top_pixel == (128, 128, 128)

    def test_resize_with_tuple_size(self, tmp_path: Path) -> None:
        """tupleでサイズ指定できることを確認."""
        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (300, 200), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "output.jpg"
        resize_with_padding(src, dst, size=(640, 480))

        output_img = Image.open(dst)
        assert output_img.size == (640, 480)

    def test_resize_mode_short(self, tmp_path: Path) -> None:
        """mode='short' で短辺基準のリサイズができることを確認."""
        # 200x100 の横長画像（PNGで圧縮誤差を回避）
        src = tmp_path / "input.png"
        img = Image.new("RGB", (200, 100), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "output.png"
        resize_with_padding(src, dst, size=100, mode="short")

        output_img = Image.open(dst)
        assert output_img.size == (100, 100)

        # 短辺基準なのでクロップされる（画像が埋め尽くす）
        # 左右の端も赤であること
        left_pixel = output_img.getpixel((0, 50))
        right_pixel = output_img.getpixel((99, 50))
        assert left_pixel == (255, 0, 0)
        assert right_pixel == (255, 0, 0)

    def test_resize_creates_output_directory(self, tmp_path: Path) -> None:
        """出力ディレクトリが自動作成されることを確認."""
        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (100, 100), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "nested" / "deep" / "output.jpg"
        resize_with_padding(src, dst, size=50)

        assert dst.exists()

    def test_resize_raises_on_missing_file(self, tmp_path: Path) -> None:
        """存在しないファイルでFileNotFoundErrorが発生することを確認."""
        src = tmp_path / "nonexistent.jpg"
        dst = tmp_path / "output.jpg"

        with pytest.raises(FileNotFoundError):
            resize_with_padding(src, dst, size=100)

    def test_resize_raises_on_invalid_mode(self, tmp_path: Path) -> None:
        """無効なmodeでValueErrorが発生することを確認."""
        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (100, 100), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "output.jpg"

        with pytest.raises(ValueError) as exc_info:
            resize_with_padding(src, dst, size=100, mode="invalid")

        assert "invalid" in str(exc_info.value)

    def test_resize_rgba_image(self, tmp_path: Path) -> None:
        """RGBA画像を処理できることを確認."""
        src = tmp_path / "input.png"
        img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
        img.save(src)

        dst = tmp_path / "output.jpg"
        resize_with_padding(src, dst, size=50)

        assert dst.exists()
        output_img = Image.open(dst)
        assert output_img.mode == "RGB"

    def test_resize_grayscale_image(self, tmp_path: Path) -> None:
        """グレースケール画像を処理できることを確認."""
        src = tmp_path / "input.jpg"
        img = Image.new("L", (100, 100), 128)
        img.save(src)

        dst = tmp_path / "output.jpg"
        resize_with_padding(src, dst, size=50)

        assert dst.exists()
        output_img = Image.open(dst)
        assert output_img.mode == "RGB"


class TestPochiResizeImage:
    """Pochi.resize_imageメソッドのテスト."""

    def test_resize_image_basic(self, tmp_path: Path) -> None:
        """Pochiからリサイズできることを確認."""
        pochi = Pochi()

        src = tmp_path / "input.jpg"
        img = Image.new("RGB", (200, 100), (255, 0, 0))
        img.save(src)

        dst = tmp_path / "output.jpg"
        result = pochi.resize_image(src, dst, size=100)

        assert result == dst
        assert dst.exists()

        output_img = Image.open(dst)
        assert output_img.size == (100, 100)

    def test_full_workflow_with_mirror_structure(self, tmp_path: Path) -> None:
        """mirror_structureと組み合わせた完全なワークフローを確認."""
        pochi = Pochi()

        # テスト用のフォルダ構造を作成
        (tmp_path / "data" / "cat").mkdir(parents=True)
        (tmp_path / "data" / "dog").mkdir(parents=True)

        # 画像を作成
        img1 = Image.new("RGB", (300, 200), (255, 0, 0))
        img1.save(tmp_path / "data" / "cat" / "001.jpg")

        img2 = Image.new("RGB", (200, 300), (0, 255, 0))
        img2.save(tmp_path / "data" / "cat" / "002.jpg")

        img3 = Image.new("RGB", (400, 400), (0, 0, 255))
        img3.save(tmp_path / "data" / "dog" / "001.jpg")

        # ファイルを検索
        files = pochi.find_files(tmp_path / "data", extensions=[".jpg"])
        assert len(files) == 3

        # フォルダ構造をミラーリング
        src_files, dst_files = pochi.mirror_structure(
            files, dest=tmp_path / "resized", base_dir=tmp_path / "data"
        )

        # リサイズ
        for src, dst in zip(src_files, dst_files):
            pochi.resize_image(src, dst, size=224)

        # 結果を確認
        for dst in dst_files:
            assert dst.exists()
            output_img = Image.open(dst)
            assert output_img.size == (224, 224)

        # フォルダ構造が保持されていることを確認
        assert (tmp_path / "resized" / "cat" / "001.jpg").exists()
        assert (tmp_path / "resized" / "cat" / "002.jpg").exists()
        assert (tmp_path / "resized" / "dog" / "001.jpg").exists()
