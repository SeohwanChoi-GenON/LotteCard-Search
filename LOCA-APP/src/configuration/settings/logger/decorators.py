"""
로깅 관련 데코레이터
"""
import functools
import time
from typing import Callable, Any, Optional
from .logger_config import get_logger


def log_execution_time(
        logger_name: Optional[str] = None,
        log_level: str = "INFO"
) -> Callable:
    """함수 실행 시간을 로깅하는 데코레이터"""

    def decorator(func: Callable) -> Callable:
        logger = get_logger(logger_name or func.__module__)
        log_func = getattr(logger, log_level.lower())

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                log_func(f"⏱{func.__name__}() executed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__}() failed after {execution_time:.3f}s: {e}")
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                log_func(f"{func.__name__}() executed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__}() failed after {execution_time:.3f}s: {e}")
                raise

        return async_wrapper if functools.iscoroutinefunction(func) else wrapper

    return decorator


def log_function_call(
        logger_name: Optional[str] = None,
        log_args: bool = False,
        log_result: bool = False
) -> Callable:
    """함수 호출을 로깅하는 데코레이터"""

    def decorator(func: Callable) -> Callable:
        logger = get_logger(logger_name or func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 함수 시작 로그
            if log_args:
                logger.info(f"Calling {func.__name__}() with args={args}, kwargs={kwargs}")
            else:
                logger.info(f"Calling {func.__name__}()")

            try:
                result = func(*args, **kwargs)

                # 함수 완료 로그
                if log_result:
                    logger.info(f"{func.__name__}() completed with result: {result}")
                else:
                    logger.info(f"{func.__name__}() completed successfully")

                return result

            except Exception as e:
                logger.error(f"{func.__name__}() failed: {e}")
                raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            # 함수 시작 로그
            if log_args:
                logger.info(f"Calling {func.__name__}() with args={args}, kwargs={kwargs}")
            else:
                logger.info(f"Calling {func.__name__}()")

            try:
                result = await func(*args, **kwargs)

                # 함수 완료 로그
                if log_result:
                    logger.info(f"{func.__name__}() completed with result: {result}")
                else:
                    logger.info(f"{func.__name__}() completed successfully")

                return result

            except Exception as e:
                logger.error(f"{func.__name__}() failed: {e}")
                raise

        return async_wrapper if functools.iscoroutinefunction(func) else wrapper

    return decorator