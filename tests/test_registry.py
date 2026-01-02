"""Tests for Registry functionality."""

import pytest

from pochi import Pochi
from pochi.registry import IRegistry, Registry


class TestRegistry:
    """Registryクラスのテスト."""

    def test_register_and_create(self) -> None:
        """クラスを登録してインスタンス生成できることを確認."""
        registry = Registry("test")

        @registry.register("sample")
        class Sample:
            def __init__(self, value: int = 0):
                self.value = value

        instance = registry.create("sample", value=42)

        assert instance.value == 42

    def test_register_without_args(self) -> None:
        """引数なしでインスタンス生成できることを確認."""
        registry = Registry("test")

        @registry.register("simple")
        class Simple:
            pass

        instance = registry.create("simple")

        assert isinstance(instance, Simple)

    def test_keys_returns_registered_names(self) -> None:
        """登録済み名前一覧が取得できることを確認."""
        registry = Registry("test")

        @registry.register("a")
        class A:
            pass

        @registry.register("b")
        class B:
            pass

        names = registry.keys()

        assert "a" in names
        assert "b" in names
        assert len(names) == 2

    def test_create_unregistered_raises_error(self) -> None:
        """未登録名でcreateするとValueErrorが発生することを確認."""
        registry = Registry("test")

        with pytest.raises(ValueError) as exc_info:
            registry.create("unknown")

        assert "未登録" in str(exc_info.value)
        assert "unknown" in str(exc_info.value)

    def test_duplicate_register_raises_error(self) -> None:
        """同じ名前で二重登録するとValueErrorが発生することを確認."""
        registry = Registry("test")

        @registry.register("dup")
        class First:
            pass

        with pytest.raises(ValueError) as exc_info:

            @registry.register("dup")
            class Second:
                pass

        assert "既に登録されています" in str(exc_info.value)

    def test_name_property(self) -> None:
        """レジストリ名が取得できることを確認."""
        registry = Registry("my_registry")

        assert registry.name == "my_registry"

    def test_contains(self) -> None:
        """in演算子で登録済みかチェックできることを確認."""
        registry = Registry("test")

        @registry.register("exists")
        class Exists:
            pass

        assert "exists" in registry
        assert "not_exists" not in registry

    def test_len(self) -> None:
        """len()で登録数が取得できることを確認."""
        registry = Registry("test")

        assert len(registry) == 0

        @registry.register("a")
        class A:
            pass

        assert len(registry) == 1

        @registry.register("b")
        class B:
            pass

        assert len(registry) == 2


class TestRegistryCreateFromConfig:
    """Registry.create_from_configメソッドのテスト."""

    def test_create_from_config(self) -> None:
        """設定リストから一括生成できることを確認."""
        registry = Registry("processors")

        @registry.register("blur")
        class Blur:
            def __init__(self, size: int = 3):
                self.size = size

        @registry.register("edge")
        class Edge:
            def __init__(self, threshold: int = 100):
                self.threshold = threshold

        config = [
            {"name": "blur", "size": 5},
            {"name": "edge", "threshold": 50},
        ]

        instances = registry.create_from_config(config)

        assert len(instances) == 2
        assert instances[0].size == 5
        assert instances[1].threshold == 50

    def test_create_from_config_empty_list(self) -> None:
        """空リストで空の結果が返ることを確認."""
        registry = Registry("test")

        instances = registry.create_from_config([])

        assert instances == []

    def test_create_from_config_without_name_raises_error(self) -> None:
        """nameキーがないとKeyErrorが発生することを確認."""
        registry = Registry("test")

        @registry.register("sample")
        class Sample:
            pass

        with pytest.raises(KeyError) as exc_info:
            registry.create_from_config([{"value": 1}])

        assert "name" in str(exc_info.value)

    def test_create_from_config_unregistered_raises_error(self) -> None:
        """未登録名が含まれるとValueErrorが発生することを確認."""
        registry = Registry("test")

        with pytest.raises(ValueError) as exc_info:
            registry.create_from_config([{"name": "unknown"}])

        assert "未登録" in str(exc_info.value)


class TestPochiCreateRegistry:
    """Pochi.create_registryメソッドのテスト."""

    def test_create_registry_returns_registry(self) -> None:
        """Registryインスタンスが返されることを確認."""
        pochi = Pochi()

        registry = pochi.create_registry("models")

        assert isinstance(registry, IRegistry)
        assert registry.name == "models"

    def test_create_registry_is_independent(self) -> None:
        """複数のレジストリが独立していることを確認."""
        pochi = Pochi()

        registry1 = pochi.create_registry("models")
        registry2 = pochi.create_registry("losses")

        @registry1.register("resnet")
        class ResNet:
            pass

        @registry2.register("dice")
        class DiceLoss:
            pass

        assert "resnet" in registry1
        assert "resnet" not in registry2
        assert "dice" in registry2
        assert "dice" not in registry1

    def test_full_workflow(self) -> None:
        """Pochiからの完全なワークフローを確認."""
        pochi = Pochi()
        processors = pochi.create_registry("processors")

        @processors.register("blur")
        class BlurProcessor:
            def __init__(self, kernel_size: int = 5):
                self.kernel_size = kernel_size

            def process(self, x: int) -> int:
                return x * self.kernel_size

        @processors.register("scale")
        class ScaleProcessor:
            def __init__(self, factor: int = 2):
                self.factor = factor

            def process(self, x: int) -> int:
                return x * self.factor

        config = [
            {"name": "blur", "kernel_size": 3},
            {"name": "scale", "factor": 10},
        ]

        pipeline = processors.create_from_config(config)

        # パイプライン実行
        value = 1
        for proc in pipeline:
            value = proc.process(value)

        # 1 * 3 * 10 = 30
        assert value == 30
