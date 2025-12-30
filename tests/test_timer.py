"""Tests for Timer functionality."""

import logging
import time
from unittest.mock import MagicMock

import pytest

from pochi import ITimerFactory, Pochi
from pochi.timer import TimerContext, TimerFactory


class TestTimerContext:
    """TimerContextクラスのテスト."""

    def test_measures_elapsed_time(self) -> None:
        """経過時間が計測されることを確認."""
        timer = TimerContext("test")

        with timer:
            time.sleep(0.1)

        assert timer.elapsed >= 0.1
        assert timer.elapsed < 0.2

    def test_prints_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """print出力されることを確認."""
        with TimerContext("処理A"):
            time.sleep(0.05)

        captured = capsys.readouterr()
        assert "処理A:" in captured.out
        assert "s" in captured.out

    def test_logs_output(self) -> None:
        """ロガー経由で出力されることを確認."""
        mock_logger = MagicMock(spec=logging.Logger)

        with TimerContext("処理B", logger=mock_logger):
            time.sleep(0.05)

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "処理B:" in call_args


class TestTimerFactory:
    """TimerFactoryクラスのテスト."""

    def test_create_returns_timer_context(self) -> None:
        """TimerContextが返されることを確認."""
        factory = TimerFactory()

        timer = factory.create("test")

        assert isinstance(timer, TimerContext)

    def test_create_with_logger(self) -> None:
        """ロガー付きでTimerContextが生成されることを確認."""
        factory = TimerFactory()
        mock_logger = MagicMock(spec=logging.Logger)

        with factory.create("test", logger=mock_logger):
            pass

        mock_logger.info.assert_called_once()


class TestPochiTimer:
    """Pochi.timerメソッドのテスト."""

    def test_timer_returns_context_manager(self) -> None:
        """コンテキストマネージャーが返されることを確認."""
        pochi = Pochi()

        timer = pochi.timer("test")

        assert isinstance(timer, TimerContext)

    def test_timer_measures_time(self) -> None:
        """時間が計測されることを確認."""
        pochi = Pochi()

        with pochi.timer("test") as t:
            time.sleep(0.1)

        assert t.elapsed >= 0.1

    def test_timer_with_logger(self) -> None:
        """ロガーと連携できることを確認."""
        pochi = Pochi()
        mock_logger = MagicMock(spec=logging.Logger)

        with pochi.timer("test", logger=mock_logger):
            pass

        mock_logger.info.assert_called_once()

    def test_timer_with_mock_factory(self) -> None:
        """カスタムTimerFactoryを注入できることを確認."""
        mock_factory = MagicMock(spec=ITimerFactory)
        mock_timer = MagicMock(spec=TimerContext)
        mock_factory.create.return_value = mock_timer

        pochi = Pochi(timer_factory=mock_factory)
        result = pochi.timer("test")

        assert result == mock_timer
        mock_factory.create.assert_called_once_with("test", logger=None)
