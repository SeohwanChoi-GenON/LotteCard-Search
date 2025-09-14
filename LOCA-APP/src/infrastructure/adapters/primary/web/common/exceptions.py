"""
웹 어댑터 공통 예외 클래스

웹 어댑터에서 사용하는 커스텀 예외들을 정의합니다.
"""

from typing import Optional, Dict, Any


class WebAdapterException(Exception):
    """웹 어댑터 기본 예외"""

    def __init__(
            self,
            message: str,
            error_code: str = "WEB_ADAPTER_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class ValidationException(WebAdapterException):
    """검증 실패 예외"""

    def __init__(
            self,
            message: str,
            field: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=details
        )
        self.field = field


class BusinessLogicException(WebAdapterException):
    """비즈니스 로직 예외"""

    def __init__(
            self,
            message: str,
            error_code: str = "BUSINESS_LOGIC_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            details=details
        )


class ExternalServiceException(WebAdapterException):
    """외부 서비스 호출 실패 예외"""

    def __init__(
            self,
            message: str,
            service_name: str,
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=details
        )
        self.service_name = service_name