from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class UploadOperation(str, Enum):
    """업로드 연산 타입"""
    INSERT = "Insert"
    UPDATE = "Update"
    DELETE = "Delete"


class UploadRequest(BaseModel):
    """파일 업로드 요청 스키마 (form data와 함께 사용)"""
    index_name: str = Field(
        ...,
        max_length=200,
        description="인덱스명",
        example="card_documents"
    )
    metadata: str = Field(
        ...,
        max_length=1000,
        description="적재 메타데이터 (JSON 형식)",
        example='{"category": "card", "version": "1.0", "author": "admin"}'
    )
    operator: UploadOperation = Field(
        ...,
        description="CRUD 기능 선택",
        example="Insert"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "index_name": "card_documents",
                "metadata": '{"category": "card", "version": "1.0", "author": "admin"}',
                "operator": "Insert"
            }
        }