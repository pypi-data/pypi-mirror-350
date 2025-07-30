import asyncio
import logging
from typing import Any, cast
from unittest import TestCase

from sag_py_execution_time_decorator.execution_time_decorator import _calculate_and_log_execution_time
from tests.test_data import (
    SLEEP_TIME_MS,
    decorated_async_method,
    decorated_async_method_extra_params,
    decorated_sync_method,
    decorated_sync_method_extra_params,
)


class PredictionControllerTest(TestCase):
    def test_log_execution_time_sync_function(self) -> None:
        # Act
        with self.assertLogs() as log_watcher:
            actual = decorated_sync_method("input")

            # Assert
            log_record = cast(Any, log_watcher.records[0])
            self.assertAlmostEqual(log_record.execution_time, SLEEP_TIME_MS, delta=100)
            self.assertEqual(log_record.function_name, "decorated_sync_method")
            self.assertEqual(log_record.levelname, "INFO")
            self.assertEqual(actual, "test: input")

    def test_log_execution_time_async_function(self) -> None:
        # Arrange
        loop = asyncio.get_event_loop()

        # Act
        with self.assertLogs() as log_watcher:
            actual = loop.run_until_complete(decorated_async_method("input"))

            # Assert
            log_record = cast(Any, log_watcher.records[0])
            self.assertAlmostEqual(log_record.execution_time, SLEEP_TIME_MS, delta=100)
            self.assertEqual(log_record.function_name, "decorated_async_method")
            self.assertEqual(log_record.levelname, "ERROR")
            self.assertEqual(actual, "test: input")
            self.assertTrue("param" not in log_record.__dict__.keys())

    def test__calculate_and_log_execution_time(self) -> None:
        # Act
        with self.assertLogs() as log_watcher:
            _calculate_and_log_execution_time(1683537228701, 1683537229702, "my_logger", logging.INFO, "my_func_name")

            # Assert
            log_record = cast(Any, log_watcher.records[0])
            self.assertEqual(log_record.execution_time, 1001)
            self.assertEqual(log_record.name, "my_logger")
            self.assertEqual(log_record.levelname, "INFO")
            self.assertEqual(log_record.function_name, "my_func_name")
            self.assertTrue("param" not in log_record.__dict__.keys())

    def test_log_execution_time_sync_extra_params_function(self) -> None:
        # Act
        with self.assertLogs() as log_watcher:
            actual = decorated_sync_method_extra_params("input")

            # Assert
            log_record = cast(Any, log_watcher.records[0])
            self.assertAlmostEqual(log_record.execution_time, SLEEP_TIME_MS, delta=100)
            self.assertEqual(log_record.function_name, "decorated_sync_method_extra_params")
            self.assertEqual(log_record.levelname, "INFO")
            assert set({"param": "input"}.items()).issubset(set(log_record.__dict__.items()))
            self.assertTrue("foo" not in log_record.__dict__.keys())
            self.assertEqual(actual, "test: input")

    def test_log_execution_time_async_extra_params_function(self) -> None:
        # Arrange
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Act
        with self.assertLogs() as log_watcher:
            actual = loop.run_until_complete(decorated_async_method_extra_params("input"))

            # Assert
            log_record = cast(Any, log_watcher.records[0])
            self.assertAlmostEqual(log_record.execution_time, SLEEP_TIME_MS, delta=100)
            self.assertEqual(log_record.function_name, "decorated_async_method_extra_params")
            self.assertEqual(log_record.levelname, "INFO")
            assert set({"param": "input"}.items()).issubset(set(log_record.__dict__.items()))
            self.assertEqual(actual, "test: input")
