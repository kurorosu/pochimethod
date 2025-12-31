"""config モジュールのテスト."""

import pytest
from pydantic import BaseModel, ValidationError

from pochi import Pochi
from pochi.config import (
    ConfigLoaderFacade,
    IConfigLoader,
    JsonConfigLoader,
    PythonConfigLoader,
    YamlConfigLoader,
)


class SampleConfig(BaseModel):
    """テスト用の設定モデル."""

    model_name: str
    epochs: int
    learning_rate: float = 0.001


class TestPythonConfigLoader:
    """PythonConfigLoader のテスト."""

    def test_supports_py_file(self) -> None:
        """拡張子 .py をサポートする."""
        loader = PythonConfigLoader()
        assert loader.supports("config.py") is True
        assert loader.supports("path/to/config.py") is True

    def test_not_supports_other_extensions(self) -> None:
        """他の拡張子はサポートしない."""
        loader = PythonConfigLoader()
        assert loader.supports("config.json") is False
        assert loader.supports("config.yaml") is False
        assert loader.supports("config.toml") is False

    def test_load_python_config(self, tmp_path: pytest.TempPathFactory) -> None:
        """Python 設定ファイルを読み込める."""
        config_file = tmp_path / "config.py"
        config_file.write_text(
            'model_name = "resnet18"\nepochs = 100\nlearning_rate = 0.001\n'
        )

        loader = PythonConfigLoader()
        config = loader.load(str(config_file))

        assert config["model_name"] == "resnet18"
        assert config["epochs"] == 100
        assert config["learning_rate"] == 0.001

    def test_load_excludes_private_variables(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """アンダースコアで始まる変数は除外される."""
        config_file = tmp_path / "config.py"
        config_file.write_text('public_var = "hello"\n_private_var = "secret"\n')

        loader = PythonConfigLoader()
        config = loader.load(str(config_file))

        assert "public_var" in config
        assert "_private_var" not in config

    def test_load_file_not_found(self) -> None:
        """存在しないファイルで FileNotFoundError."""
        loader = PythonConfigLoader()
        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent.py")

    def test_load_syntax_error(self, tmp_path: pytest.TempPathFactory) -> None:
        """構文エラーのファイルで ValueError."""
        config_file = tmp_path / "bad_config.py"
        config_file.write_text("invalid syntax here !!!")

        loader = PythonConfigLoader()
        with pytest.raises(ValueError, match="構文エラー"):
            loader.load(str(config_file))


class TestJsonConfigLoader:
    """JsonConfigLoader のテスト."""

    def test_supports_json_file(self) -> None:
        """拡張子 .json をサポートする."""
        loader = JsonConfigLoader()
        assert loader.supports("config.json") is True
        assert loader.supports("path/to/config.json") is True

    def test_not_supports_other_extensions(self) -> None:
        """他の拡張子はサポートしない."""
        loader = JsonConfigLoader()
        assert loader.supports("config.py") is False
        assert loader.supports("config.yaml") is False
        assert loader.supports("config.toml") is False

    def test_load_json_config(self, tmp_path: pytest.TempPathFactory) -> None:
        """JSON 設定ファイルを読み込める."""
        config_file = tmp_path / "config.json"
        config_file.write_text(
            '{"model_name": "resnet18", "epochs": 100, "learning_rate": 0.001}'
        )

        loader = JsonConfigLoader()
        config = loader.load(str(config_file))

        assert config["model_name"] == "resnet18"
        assert config["epochs"] == 100
        assert config["learning_rate"] == 0.001

    def test_load_file_not_found(self) -> None:
        """存在しないファイルで FileNotFoundError."""
        loader = JsonConfigLoader()
        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent.json")

    def test_load_syntax_error(self, tmp_path: pytest.TempPathFactory) -> None:
        """構文エラーのファイルで ValueError."""
        config_file = tmp_path / "bad_config.json"
        config_file.write_text("{invalid json}")

        loader = JsonConfigLoader()
        with pytest.raises(ValueError, match="JSON"):
            loader.load(str(config_file))

    def test_load_non_object_root(self, tmp_path: pytest.TempPathFactory) -> None:
        """ルートがオブジェクトでない場合に ValueError."""
        config_file = tmp_path / "array_config.json"
        config_file.write_text("[1, 2, 3]")

        loader = JsonConfigLoader()
        with pytest.raises(ValueError, match="オブジェクト"):
            loader.load(str(config_file))


class TestYamlConfigLoader:
    """YamlConfigLoader のテスト."""

    def test_supports_yaml_file(self) -> None:
        """拡張子 .yaml と .yml をサポートする."""
        loader = YamlConfigLoader()
        assert loader.supports("config.yaml") is True
        assert loader.supports("config.yml") is True
        assert loader.supports("path/to/config.yaml") is True

    def test_not_supports_other_extensions(self) -> None:
        """他の拡張子はサポートしない."""
        loader = YamlConfigLoader()
        assert loader.supports("config.py") is False
        assert loader.supports("config.json") is False
        assert loader.supports("config.toml") is False

    def test_load_yaml_config(self, tmp_path: pytest.TempPathFactory) -> None:
        """YAML 設定ファイルを読み込める."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "model_name: resnet18\nepochs: 100\nlearning_rate: 0.001\n"
        )

        loader = YamlConfigLoader()
        config = loader.load(str(config_file))

        assert config["model_name"] == "resnet18"
        assert config["epochs"] == 100
        assert config["learning_rate"] == 0.001

    def test_load_empty_file(self, tmp_path: pytest.TempPathFactory) -> None:
        """空ファイルは空の dict を返す."""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        loader = YamlConfigLoader()
        config = loader.load(str(config_file))

        assert config == {}

    def test_load_file_not_found(self) -> None:
        """存在しないファイルで FileNotFoundError."""
        loader = YamlConfigLoader()
        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent.yaml")

    def test_load_syntax_error(self, tmp_path: pytest.TempPathFactory) -> None:
        """構文エラーのファイルで ValueError."""
        config_file = tmp_path / "bad_config.yaml"
        config_file.write_text("key: [unclosed bracket")

        loader = YamlConfigLoader()
        with pytest.raises(ValueError, match="YAML"):
            loader.load(str(config_file))

    def test_load_non_object_root(self, tmp_path: pytest.TempPathFactory) -> None:
        """ルートがオブジェクトでない場合に ValueError."""
        config_file = tmp_path / "array_config.yaml"
        config_file.write_text("- item1\n- item2\n")

        loader = YamlConfigLoader()
        with pytest.raises(ValueError, match="オブジェクト"):
            loader.load(str(config_file))


class TestConfigLoaderFacade:
    """ConfigLoaderFacade のテスト."""

    def test_load_with_validation(self, tmp_path: pytest.TempPathFactory) -> None:
        """Pydantic モデルでバリデーションできる."""
        config_file = tmp_path / "config.py"
        config_file.write_text(
            'model_name = "resnet18"\nepochs = 100\nlearning_rate = 0.001\n'
        )

        facade = ConfigLoaderFacade()
        config = facade.load(str(config_file), SampleConfig)

        assert isinstance(config, SampleConfig)
        assert config.model_name == "resnet18"
        assert config.epochs == 100
        assert config.learning_rate == 0.001

    def test_load_with_default_value(self, tmp_path: pytest.TempPathFactory) -> None:
        """デフォルト値が適用される."""
        config_file = tmp_path / "config.py"
        config_file.write_text('model_name = "resnet18"\nepochs = 100\n')

        facade = ConfigLoaderFacade()
        config = facade.load(str(config_file), SampleConfig)

        assert config.learning_rate == 0.001  # デフォルト値

    def test_load_validation_error(self, tmp_path: pytest.TempPathFactory) -> None:
        """バリデーションエラーで例外."""
        config_file = tmp_path / "config.py"
        config_file.write_text('model_name = "resnet18"\nepochs = "not_an_int"\n')

        facade = ConfigLoaderFacade()
        with pytest.raises(ValidationError):
            facade.load(str(config_file), SampleConfig)

    def test_load_strict_mode_rejects_type_coercion(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """strict モードで型の自動変換を拒否する."""
        config_file = tmp_path / "config.py"
        # epochs が文字列 "100" (int に変換可能だが strict では拒否)
        config_file.write_text('model_name = "resnet18"\nepochs = "100"\n')

        facade = ConfigLoaderFacade()
        with pytest.raises(ValidationError):
            facade.load(str(config_file), SampleConfig)

    def test_load_unsupported_format(self) -> None:
        """サポートされていない形式で ValueError."""
        facade = ConfigLoaderFacade()
        with pytest.raises(ValueError, match="サポートされていない"):
            facade.load("config.toml", SampleConfig)

    def test_load_dict(self, tmp_path: pytest.TempPathFactory) -> None:
        """dict として読み込める."""
        config_file = tmp_path / "config.py"
        config_file.write_text('model_name = "resnet18"\nepochs = 100\n')

        facade = ConfigLoaderFacade()
        config = facade.load_dict(str(config_file))

        assert isinstance(config, dict)
        assert config["model_name"] == "resnet18"
        assert config["epochs"] == 100


class TestPochiLoadConfig:
    """Pochi.load_config のテスト."""

    def test_load_config(self, tmp_path: pytest.TempPathFactory) -> None:
        """Pochi から設定を読み込める."""
        config_file = tmp_path / "config.py"
        config_file.write_text(
            'model_name = "resnet18"\nepochs = 100\nlearning_rate = 0.001\n'
        )

        pochi = Pochi()
        config = pochi.load_config(str(config_file), SampleConfig)

        assert isinstance(config, SampleConfig)
        assert config.model_name == "resnet18"
        assert config.epochs == 100
