"""
컨텐츠 관련 스키마

검색된 컨텐츠 등 데이터 관련 스키마를 정의합니다.
"""
from pydantic import BaseModel, Field


class RetrievedContent(BaseModel):
    """검색된 컨텐츠 공통 스키마"""
    document_id: str = Field(
        ...,
        description="문서 ID",
        example="doc_001"
    )
    title: str = Field(
        ...,
        description="문서 제목",
        example="롯데카드 혜택 안내"
    )
    content: str = Field(
        ...,
        description="문서 내용",
        example="롯데카드를 이용하면 다양한 혜택을..."
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="관련도 점수",
        example=0.95
    )
    source: str = Field(
        ...,
        description="문서 출처",
        example="card_database"
    )