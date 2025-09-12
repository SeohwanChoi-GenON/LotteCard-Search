from enum import Enum

from pydantic import BaseModel, Field

from interfaces.api.schemas.search.context.context_schema import SearchContextResponse
from interfaces.api.schemas.search.data.data_schema import SearchDataResponse
from interfaces.api.schemas.search.meta.meta_schema import SearchMetaResponse


class ServiceType(str, Enum):
    """서비스 타입 열거형"""
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"

class SearchRequest(BaseModel):
    """LOCA 챗봇 요청 스키마"""
    thread_id: str = Field(..., max_length=50, description="대화 세션 고유 ID")
    user_id: str = Field(..., max_length=20, description="사용자 ID")
    service_id: ServiceType = Field(..., description="서비스 식별자")
    user_input: str = Field(..., max_length=1000, description="사용자 질문 내용")

class SearchResponse(BaseModel):
    """LOCA 챗봇 응답 스키마"""
    meta: SearchMetaResponse
    data: SearchDataResponse
    context: SearchContextResponse
