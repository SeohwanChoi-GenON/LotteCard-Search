from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional
from datetime import datetime

T = TypeVar('T')

class GatewayComm(BaseModel):
    """API Gateway 공통 헤더"""
    GUID: str = Field(..., description="Global Unique ID")
    SRC_SYS_CD: str = Field("GAI", description="출발지 시스템 코드")
    STC_BIZ_CDD: str = Field("BR", description="출발지 업무 코드")
    GRAM_PRG_NO: str = Field("00", description="전문 진행번호")
    GRAN_NO: str = Field("N", description="전문 번호")
    TSMT: str = Field(..., description="요청 타임스탬프")

class GatewayRequest(BaseModel, Generic[T]):
    """Gateway 요청 wrapper"""
    COMM: GatewayComm
    data: T

class GatewayResponse(BaseModel, Generic[T]):
    """Gateway 응답 wrapper"""
    COMM: GatewayComm
    data: T
    result_code: str = Field("0000", description="결과 코드")
    result_message: str = Field("성공", description="결과 메시지")