# pochimethod

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
