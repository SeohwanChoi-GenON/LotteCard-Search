from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ServiceType(str, Enum):
    """서비스 타입 열거형"""
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"

class BaseMetaResponse(BaseModel):
    """기본 응답 메타데이터"""
    result_status: str = Field(..., max_length=20, description="처리 상태")
    result_status_message: str = Field(..., max_length=1000, description="처리 상태 메시지")
    timestamp: datetime = Field(..., description="타임스탬프")
