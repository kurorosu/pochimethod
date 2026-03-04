# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Workspace に `__dir__` を追加し IDE 補完を改善 ([#22](https://github.com/kurorosu/pochimethod/pull/22))
- TimerContext で例外発生時に warning ログを出力 ([#23](https://github.com/kurorosu/pochimethod/pull/23))
- JsonConfigLoader, YamlConfigLoader を追加 ([#24](https://github.com/kurorosu/pochimethod/pull/24))
- `mirror_structure` メソッドを追加 ([#25](https://github.com/kurorosu/pochimethod/pull/25))
- 汎用クラスレジストリ機能を追加 ([#29](https://github.com/kurorosu/pochimethod/pull/29))
- `create_workspace` に `prefix` 引数を追加して連番ディレクトリ生成に対応 ([#31](https://github.com/kurorosu/pochimethod/pull/31))
- アスペクト比保持リサイズ機能を追加 ([#35](https://github.com/kurorosu/pochimethod/pull/35))
- GitHub Issue/PR テンプレートを追加 ([#37](https://github.com/kurorosu/pochimethod/pull/37))
- Image リサイズのサンプルコード `examples/image/resize_with_padding.py` を追加

### Changed

- README にバッジと新機能ドキュメントを追加 ([#36](https://github.com/kurorosu/pochimethod/pull/36))

### Fixed

- ロガー名プレフィックスの二重付与を防止 ([#27](https://github.com/kurorosu/pochimethod/pull/27))
- リサイズ時の 1px ズレを `round()` + クランプで修正

## [0.0.2] - 2025-12-31

### Added

- `IConfigLoader` インターフェースを追加 ([#6](https://github.com/kurorosu/pochimethod/pull/6))
- `PythonConfigLoader` を実装, strict モードをデフォルトに設定 ([#6](https://github.com/kurorosu/pochimethod/pull/6))
- `Pochi` クラスに `load_config` メソッドを追加 ([#6](https://github.com/kurorosu/pochimethod/pull/6))
- `IFileFinder`, `IFileCopier` インターフェースを追加 ([#8](https://github.com/kurorosu/pochimethod/pull/8))
- `GlobFileFinder`, `StructurePreservingCopier` を実装 ([#8](https://github.com/kurorosu/pochimethod/pull/8))
- `Pochi` クラスに `find_files`, `copy_files`, `move_files` を追加 ([#8](https://github.com/kurorosu/pochimethod/pull/8))

### Changed

- `__all__` を `Pochi` のみに変更し学習コストを低減 ([#6](https://github.com/kurorosu/pochimethod/pull/6))
- README に FileOps セクションを追加 ([#21](https://github.com/kurorosu/pochimethod/pull/21))
- PythonConfigLoader のセキュリティ警告を追加 ([#17](https://github.com/kurorosu/pochimethod/pull/17))

### Fixed

- ロガー名に `pochi.` プレフィックスを追加し他ライブラリとの衝突を防止 ([#18](https://github.com/kurorosu/pochimethod/pull/18))
- FileHandler 作成前にログディレクトリを自動作成 ([#19](https://github.com/kurorosu/pochimethod/pull/19))
- PythonConfigLoader のモジュール名をファイル名から生成 ([#20](https://github.com/kurorosu/pochimethod/pull/20))

## Archived Changelogs

Older version histories are archived in the [`changelogs/`](changelogs/) directory.
