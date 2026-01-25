# pochimethod

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Pythonのための便利メソッド集 — ポチのお気に入りの骨、全部ここに！

## インストール

```bash
# pip
pip install git+https://github.com/torikatsu923/pochimethod.git

# uv
uv add git+https://github.com/torikatsu923/pochimethod.git
```

## 使い方

```python
from pochi import Pochi

pochi = Pochi()
```

### Workspace

タイムスタンプ付きの出力ディレクトリを作成します。

```python
# outputs/ ディレクトリのみ作成
ws = pochi.create_workspace()

# outputs/yyyymmdd_001/ とサブディレクトリを作成
ws = pochi.create_workspace("outputs", ["logs", "models"])

print(ws.root)    # outputs/yyyymmdd_001/ へのPath
print(ws.logs)    # outputs/yyyymmdd_001/logs/ へのPath
print(ws.models)  # outputs/yyyymmdd_001/models/ へのPath
```

### Logger

色付きコンソール出力とファイル出力に対応したロガーを作成します。

```python
# コンソールのみ（色付き）
logger = pochi.get_logger("app")

# コンソール + ファイル出力（Workspaceと連携）
ws = pochi.create_workspace("outputs", ["logs"])
logger = pochi.get_logger("training", ws.logs)

logger.info("学習を開始します...")
logger.warning("学習率が低すぎる可能性があります")
logger.error("学習に失敗しました")
```

### Config

Python 設定ファイル (.py) を読み込み、Pydantic モデルでバリデーションします。

```python
from pydantic import BaseModel

class TrainConfig(BaseModel):
    model_name: str
    epochs: int
    learning_rate: float = 0.001

config = pochi.load_config("config.py", TrainConfig)
print(config.epochs)  # 100
```

> **⚠️ セキュリティ警告**: `load_config` は Python ファイルを実行するため、信頼できないソースからの設定ファイルを読み込むと任意コード実行のリスクがあります。自分で作成した設定ファイル、またはコードレビュー済みのファイルのみを使用してください。

### FileOps

ファイルの検索・コピー・移動を行います。階層構造を保持したコピーも可能です。

```python
# ファイル検索
files = pochi.find_files("data/", pattern="**/*.jpg")

# 階層構造を保持してコピー
result = pochi.copy_files("data/", "backup/", pattern="**/*.jpg")
# data/train/cat/001.jpg → backup/train/cat/001.jpg

# 移動も同様
result = pochi.move_files("temp/", "archive/", pattern="**/*.log")
```

### Image

アスペクト比を保持して画像をリサイズし、足りない部分をパディングで埋めます。CNN学習用データセットの前処理に便利です。

```python
# 画像を検索
files = pochi.find_files("data/train", extensions=[".jpg", ".png"])

# フォルダ構造をミラーリング
src_files, dst_files = pochi.mirror_structure(
    files, dest="data_resized/train", base_dir="data/train"
)

# アスペクト比を保持して 224x224 にリサイズ
for src, dst in zip(src_files, dst_files):
    pochi.resize_image(src, dst, size=224)
```

### Registry

デコレータベースでクラスを登録し、設定ファイルから動的にインスタンスを生成します。

```python
# レジストリを作成
processors = pochi.create_registry("processors")

# クラスを登録
@processors.register("blur")
class BlurProcessor:
    def __init__(self, kernel_size: int = 5):
        self.kernel_size = kernel_size

@processors.register("edge")
class EdgeProcessor:
    def __init__(self, threshold: int = 100):
        self.threshold = threshold

# 名前から生成
blur = processors.create("blur", kernel_size=7)

# 設定リストから一括生成
config = [
    {"name": "blur", "kernel_size": 7},
    {"name": "edge", "threshold": 50},
]
pipeline = processors.create_from_config(config)
```

### Timer

コンテキストマネージャーで処理時間を計測します。

```python
# print出力
with pochi.timer("処理"):
    do_something()

# ロガー出力
with pochi.timer("処理", logger):
    do_something()

# 経過時間を取得
with pochi.timer("処理") as t:
    do_something()
print(f"経過時間: {t.elapsed:.3f}秒")
```

## 動作環境

- Python >= 3.13

## ライセンス

MIT
