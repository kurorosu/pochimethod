"""Tests for Logging functionality."""

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pochi import Pochi
from pochi.logging import ILoggerFactory, LoggerFactory
from pochi.logging.formatters import ColoredFormatter, PlainFormatter
from pochi.logging.handlers import create_console_handler, create_file_handler


class TestFormatters:
    """フォーマッタークラスのテスト."""

    def test_colored_formatter_adds_color(self) -> None:
        """ColoredFormatterが色コードを追加することを確認."""
        formatter = ColoredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)

        # 色コードが含まれていることを確認
        assert "\033[" in result
        assert "test message" in result

    def test_plain_formatter_no_color(self) -> None:
        """PlainFormatterが色コードを追加しないことを確認."""
        formatter = PlainFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)

        # 色コードが含まれていないことを確認
        assert "\033[" not in result
        assert "test message" in result


class TestHandlers:
    """ハンドラー生成関数のテスト."""

    def test_create_console_handler(self) -> None:
        """コンソールハンドラーが生成されることを確認."""
        handler = create_console_handler()

        assert isinstance(handler, logging.StreamHandler)
        assert isinstance(handler.formatter, ColoredFormatter)

    def test_create_file_handler(self, tmp_path: Path) -> None:
        """ファイルハンドラーが生成されることを確認."""
        log_path = tmp_path / "test.log"
        handler = create_file_handler(log_path)

        assert isinstance(handler, logging.FileHandler)
        assert isinstance(handler.formatter, PlainFormatter)


class TestLoggerFactory:
    """LoggerFactoryクラスのテスト."""

    def test_create_console_only(self) -> None:
        """コンソールのみのロガーが生成されることを確認."""
        factory = LoggerFactory()

        logger = factory.create("test_console")

        assert isinstance(logger, logging.Logger)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.StreamHandler)

    def test_create_with_file(self, tmp_path: Path) -> None:
        """ファイル出力付きロガーが生成されることを確認."""
        factory = LoggerFactory()

        logger = factory.create("test_file", log_dir=tmp_path)

        assert len(logger.handlers) == 2
        # コンソールハンドラー
        assert isinstance(logger.handlers[0], logging.StreamHandler)
        # ファイルハンドラー
        assert isinstance(logger.handlers[1], logging.FileHandler)

    def test_create_writes_to_file(self, tmp_path: Path) -> None:
        """ロガーがファイルに書き込むことを確認."""
        factory = LoggerFactory()
        logger = factory.create("test_write", log_dir=tmp_path)

        logger.info("test message")

        log_file = tmp_path / "test_write.log"
        assert log_file.exists()
        content = log_file.read_text()
        assert "test message" in content

    def test_create_returns_cached_logger(self) -> None:
        """同じ設定で同じロガーが返されることを確認."""
        factory = LoggerFactory()

        logger1 = factory.create("test_cache")
        logger2 = factory.create("test_cache")

        assert logger1 is logger2


class TestPochiGetLogger:
    """Pochi.get_loggerメソッドのテスト."""

    def test_get_logger_console_only(self) -> None:
        """コンソールのみのロガーが取得できることを確認."""
        pochi = Pochi()

        logger = pochi.get_logger("test_pochi")

        assert isinstance(logger, logging.Logger)

    def test_get_logger_with_workspace(self, tmp_path: Path) -> None:
        """Workspaceと連携したロガーが取得できることを確認."""
        pochi = Pochi()
        ws = pochi.create_workspace(tmp_path, subdirs=["logs"])

        logger = pochi.get_logger("test_ws", ws.logs)
        logger.info("workspace log test")

        log_file = ws.logs / "test_ws.log"
        assert log_file.exists()
        content = log_file.read_text()
        assert "workspace log test" in content

    def test_get_logger_with_mock_factory(self) -> None:
        """カスタムLoggerFactoryを注入できることを確認."""
        mock_factory = MagicMock(spec=ILoggerFactory)
        mock_logger = MagicMock(spec=logging.Logger)
        mock_factory.create.return_value = mock_logger

        pochi = Pochi(logger_factory=mock_factory)
        result = pochi.get_logger("test", level=logging.DEBUG)

        assert result == mock_logger
        mock_factory.create.assert_called_once_with(
            "test", log_dir=None, level=logging.DEBUG
        )
