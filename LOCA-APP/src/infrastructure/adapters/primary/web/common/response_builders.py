"""
웹 어댑터 공통 응답 빌더

표준화된 응답을 빌드하는 헬퍼 함수들을 제공합니다.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from infrastructure.adapters.primary.web.common.schemas.base_schemas import ErrorResponse


class ResponseBuilder:
    """공통 응답 빌드 헬퍼 클래스"""
    @staticmethod
    def build_success_meta(
            thread_id: str,
            message_id: Optional[int] = None,
            custom_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """성공 메타 정보 빌드"""
        meta_data = {
            "thread_id": thread_id,
            "result_status": "200",
            "result_status_message": custom_message or "성공",
            "timestamp": datetime.now()
        }

        if message_id is not None:
            meta_data["message_id"] = message_id

        return meta_data

    @staticmethod
    def build_error_response(
            error_code: str,
            error_message: str,
            details: Optional[Dict[str, Any]] = None
    ) -> ErrorResponse:
        """에러 응답 빌드"""
        return ErrorResponse(
            error_code=error_code,
            error_message=error_message,
            details=details or {}
        )

    @staticmethod
    def build_validation_error(
            message: str,
            thread_id: Optional[str] = None
    ) -> ErrorResponse:
        """검증 에러 응답 빌드"""
        details = {"thread_id": thread_id} if thread_id else {}
        return ResponseBuilder.build_error_response(
            error_code="VALIDATION_ERROR",
            error_message=message,
            details=details
        )

    @staticmethod
    def build_internal_error(
            message: str = "내부 서버 오류가 발생했습니다.",
            thread_id: Optional[str] = None
    ) -> ErrorResponse:
        """내부 서버 에러 응답 빌드"""
        details = {"thread_id": thread_id} if thread_id else {}
        return ResponseBuilder.build_error_response(
            error_code="INTERNAL_ERROR",
            error_message=message,
            details=details
        )
