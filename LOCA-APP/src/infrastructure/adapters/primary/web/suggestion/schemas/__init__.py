"""
Suggestion 스키마 모듈

연관질문 관련 요청/응답 스키마들을 내보냅니다.
"""

from .request_schema import SuggestionRequest
from .response_schema import (
    SuggestionResponse,
    SuggestionResponseMeta,
    SuggestionResponseData
)
from ...common.base_schemas import ErrorResponse

__all__ = [
    "SuggestionRequest",
    "SuggestionResponse",
    "SuggestionResponseMeta",
    "SuggestionResponseData",
    "ErrorResponse"
]