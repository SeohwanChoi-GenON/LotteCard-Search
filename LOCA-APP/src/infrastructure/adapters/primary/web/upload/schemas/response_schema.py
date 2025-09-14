from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class UploadResponseMeta(BaseModel):
    """업로드 응답 메타데이터"""
    upload_id: str = Field(..., max_length=50, description="업로드 세션 고유 ID")
    result_status: str = Field(..., max_length=20, description="처리 상태")
    result_status_message: str = Field(..., max_length=1000, description="처리 상태 메시지")
    timestamp: datetime = Field(..., description="타임스탬프")


class UploadData(BaseModel):
    """업로드 응답 데이터"""
    document_id: str = Field(..., description="생성/수정된 문서 ID")
    created_at: datetime = Field(..., description="문서의 생성된 시간")
    index_name: Optional[str] = Field(None, description="적재된 인덱스명")
    operation: Optional[str] = Field(None, description="수행된 연산")
    file_info: Optional[Dict[str, Any]] = Field(None, description="파일 정보")


class UploadResponse(BaseModel):
    """업로드 응답 스키마"""
    meta: UploadResponseMeta
    data: UploadData

    class Config:
        json_schema_extra = {
            "example": {
                "meta": {
                    "upload_id": "upload_12345",
                    "result_status": "200",
                    "result_status_message": "업로드 성공",
                    "timestamp": "2025-09-15T00:30:00Z"
                },
                "data": {
                    "document_id": "doc_uploaded_001",
                    "created_at": "2025-09-15T00:30:00Z",
                    "index_name": "card_documents",
                    "operation": "Insert",
                    "file_info": {
                        "filename": "card_info.pdf",
                        "size": 1024000,
                        "content_type": "application/pdf"
                    }
                }
            }
        }