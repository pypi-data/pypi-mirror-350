import asyncio
import logging
import time

from sag_py_execution_time_decorator.execution_time_decorator import log_execution_time

SLEEP_TIME_MS: int = 1000


@log_execution_time()
def decorated_sync_method(param: str) -> str:
    time.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"


@log_execution_time(log_level=logging.ERROR)
async def decorated_async_method(param: str) -> str:
    await asyncio.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"


@log_execution_time(log_params=("param", "foo"))
def decorated_sync_method_extra_params(param: str) -> str:
    time.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"


@log_execution_time(log_params=("param",))
async def decorated_async_method_extra_params(param: str) -> str:
    await asyncio.sleep(SLEEP_TIME_MS / 1000)
    return f"test: {param}"
