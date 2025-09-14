"""
웹 어댑터 공통 데코레이터

로깅, 예외 처리 등 공통 기능을 제공하는 데코레이터들을 정의합니다.
"""

import logging
import functools
from typing import Callable, Any
from fastapi import HTTPException, status
from .response_builders import ResponseBuilder

logger = logging.getLogger(__name__)


def handle_exceptions(func: Callable) -> Callable:
    """공통 예외 처리 데코레이터"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            error_response = ResponseBuilder.build_validation_error(str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response.model_dump()
            )
        except HTTPException:
            # FastAPI HTTPException은 그대로 전파
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            error_response = ResponseBuilder.build_internal_error(
                "처리 중 예상치 못한 오류가 발생했습니다."
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response.model_dump()
            )

    return wrapper


def log_request_response(func: Callable) -> Callable:
    """요청/응답 로깅 데코레이터"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        # 요청 로깅
        request = None
        for arg in args:
            if hasattr(arg, 'thread_id'):
                request = arg
                break

        if request:
            logger.info(f"Processing {func.__name__} request for thread_id: {request.thread_id}")
        else:
            logger.info(f"Processing {func.__name__} request")

        # 함수 실행
        result = await func(*args, **kwargs)

        # 응답 로깅
        if request:
            logger.info(f"Completed {func.__name__} for thread_id: {request.thread_id}")
        else:
            logger.info(f"Completed {func.__name__}")

        return result

    return wrapper


def validate_request(func: Callable) -> Callable:
    """요청 데이터 검증 데코레이터"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        # 요청 객체 찾기
        request = None
        for arg in args:
            if hasattr(arg, 'thread_id') and hasattr(arg, 'user_id'):
                request = arg
                break

        if request:
            # 공통 검증 수행
            from .validators import validate_thread_id, validate_user_id, validate_service_id

            validate_thread_id(request.thread_id)
            validate_user_id(request.user_id)
            validate_service_id(request.service_id.value)

        return await func(*args, **kwargs)

    return wrapper