from pydantic import BaseModel, Field


class GatewayComm(BaseModel):
    """API Gateway 공통 통신 헤더"""
    GUID: str = Field(..., description="Global Unique ID")
    SRC_SYS_CD: str = Field("LOC", description="출발지 시스템 코드")
    STC_BIZ_CDD: str = Field("CH", description="출발지 업무 코드")
    GRAM_PRG_NO: str = Field("00", description="전문 진행번호")
    GRAN_NO: str = Field("N", description="전문 번호")
    TSMT: str = Field(..., description="요청 타임스탬프")
