import logging
import functools
from typing import Callable, Any
from fastapi import HTTPException, status, Request, Response
from .response_builders import ResponseBuilder

logger = logging.getLogger(__name__)


def handle_exceptions(func: Callable) -> Callable:
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


def handle_gateway_integration(func):
    """API Gateway 통합 처리 데코레이터"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # 1. args에서 찾기
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                logger.info(f"Found Request in args: {type(arg)}")
            elif isinstance(arg, Response):
                response = arg
                logger.info(f"Found Response in args: {type(arg)}")

        # 2. kwargs에서 찾기 (FastAPI dependency injection 경우)
        for key, value in kwargs.items():
            if isinstance(value, Request):
                request = value
                logger.info(f"Found Request in kwargs[{key}]: {type(value)}")
            elif isinstance(value, Response):
                response = value
                logger.info(f"Found Response in kwargs[{key}]: {type(value)}")

        if not request:
            logger.error("No Request object found!")
            logger.error(f"  Args: {[type(arg) for arg in args]}")
            logger.error(f"  Kwargs: {[(k, type(v)) for k, v in kwargs.items()]}")

        gateway_info = None
        if request:
            logger.info("Starting Gateway header extraction...")
            from .gateway.schemas.gateway_middleware import GatewayProcessor
            try:
                gateway_info = await GatewayProcessor.extract_gateway_header(request)
                logger.info(f"Gateway header extracted successfully: {gateway_info}")
            except ValueError as e:
                logger.error(f"Gateway validation failed: {e}")
                # ValueError를 그대로 전파하여 handle_exceptions에서 처리하도록 함
                raise
            except Exception as e:
                logger.error(f"Unexpected error during Gateway extraction: {e}")
                import traceback
                logger.error(traceback.format_exc())
                raise
        else:
            logger.warning("⚠No request object found, skipping Gateway extraction")

        # 원본 함수 실행
        logger.info("📞 Calling original function...")
        result = await func(*args, **kwargs)
        logger.info("Original function completed")

        # 응답 헤더에 Gateway 정보 설정
        if response and gateway_info:
            logger.info("Setting response headers...")
            from .gateway.schemas.gateway_middleware import GatewayProcessor
            GatewayProcessor.set_response_headers(response, gateway_info)
            logger.info("Response headers set")
        else:
            logger.warning(f"Skipping response headers - Response: {bool(response)}, Gateway: {bool(gateway_info)}")

        logger.info("GATEWAY DECORATOR FINISHED")
        return result

    return wrapper
