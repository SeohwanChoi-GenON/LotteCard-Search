"""
Web 어댑터 공통 라이브러리

공통 스키마, 검증, 응답 빌더, 예외 처리 등을 제공합니다.
"""

from .base_schemas import (
    ServiceId,
    BaseRequest,
    BaseResponseMeta,
    BaseResponse,
    ErrorResponse,
    RetrievedContent
)
from .validators import (
    validate_thread_id,
    validate_user_id,
    validate_service_id,
    validate_user_input,
    validate_message_id
)
from .response_builders import ResponseBuilder
from .exceptions import (
    WebAdapterException,
    ValidationException,
    BusinessLogicException,
    ExternalServiceException
)
from .decorators import (
    handle_exceptions,
    log_request_response,
    validate_request
)

__all__ = [
    # Base Schemas
    "ServiceId",
    "BaseRequest",
    "BaseResponseMeta",
    "BaseResponse",
    "ErrorResponse",
    "RetrievedContent",

    # Validators
    "validate_thread_id",
    "validate_user_id",
    "validate_service_id",
    "validate_user_input",
    "validate_message_id",

    # Response Builder
    "ResponseBuilder",

    # Exceptions
    "WebAdapterException",
    "ValidationException",
    "BusinessLogicException",
    "ExternalServiceException",

    # Decorators
    "handle_exceptions",
    "log_request_response",
    "validate_request"
]