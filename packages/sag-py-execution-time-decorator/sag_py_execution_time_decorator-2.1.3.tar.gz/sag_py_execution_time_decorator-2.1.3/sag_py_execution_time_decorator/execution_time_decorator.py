import inspect
import logging
import time
from typing import Any, Callable, TypeVar, cast

# With python 3.10 param spec can be used instead - as described here:
# https://stackoverflow.com/questions/66408662/type-annotations-for-decorators
F = TypeVar("F", bound=Callable[..., Any])


def log_execution_time(
    log_level: int = logging.INFO, logger_name: str = __name__, log_params: tuple[str, ...] = ()
) -> Callable[[F], F]:
    """This decorator logs the execution time of sync and async methods

    Args:
        log_level (int, optional): The log level used for the log message. Defaults to logging.INFO.
        logger_name (str, optional): A logger used for the log message. Defaults to __name__.
        log_params (Tuple(str), optional): Parameters of the decorated function to be logged in 'extra'.

    Returns:
        F: The return value of the original function
    """

    def decorator(func: F) -> F:
        if inspect.iscoroutinefunction(func):

            async def wrapper_async(*args: Any, **kw: Any) -> Any:
                start_time = _get_current_time()
                result = await func(*args, **kw)  # types: ignore
                end_time = _get_current_time()
                extra_params = _get_params_to_log(log_params, func, args, kw)
                _calculate_and_log_execution_time(
                    start_time, end_time, logger_name, log_level, func.__name__, extra_params
                )
                return result

            return cast(F, wrapper_async)

        else:

            def wrapper_sync(*args: Any, **kw: Any) -> Any:
                start_time = _get_current_time()
                result = func(*args, **kw)
                end_time = _get_current_time()
                extra_params = _get_params_to_log(log_params, func, args, kw)
                _calculate_and_log_execution_time(
                    start_time, end_time, logger_name, log_level, func.__name__, extra_params
                )
                return result

            return cast(F, wrapper_sync)

    return decorator


def _get_current_time() -> int:
    return round(int(time.time() * 1000))


def _calculate_and_log_execution_time(
    start_time: int,
    end_time: int,
    logger_name: str,
    log_level: int,
    func_name: str,
    extra_params: dict[str, Any] | None = None,
) -> None:
    if extra_params is None:
        extra_params = {}

    execution_time = end_time - start_time

    extra_args = {"function_name": func_name, "execution_time": execution_time}
    extra_args.update(extra_params)

    time_logger = logging.getLogger(logger_name)
    time_logger.log(log_level, "%s took %s ms.", func_name, execution_time, extra=extra_args)


def _get_params_to_log(
    log_params: tuple[str, ...], func: F, func_args: tuple[Any, ...], func_kwargs: dict[str, Any]
) -> dict[str, Any]:
    """This function filters parameters and their values of a given function and returns them as a dictionary.

    Args:
        log_params (tuple[str]): A tuple of parameter names to filter by.
        func (F): The decorated function whose arguments are considered.
        func_args (tuple): Arguments of the decorated function.
        func_kwargs (Dict): Keyword arguments of the decorated function.

    Returns:
        dict: A dictionary of key/value-pairs
    """
    params_dict_log: dict[str, Any] = {}

    if log_params:
        if len(func.__code__.co_varnames) == len(func_args):
            params_dict_log.update(zip(func.__code__.co_varnames, func_args))  # transform args to kwargs
        params_dict_log.update(func_kwargs)

    return {k: v for k, v in params_dict_log.items() if k in log_params}
