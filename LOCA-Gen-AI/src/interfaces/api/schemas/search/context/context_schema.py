from typing import Optional, List

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """문서 메타데이터"""
    chunk_id: str = Field(..., description="청크 ID")
    section_name: str = Field(..., description="섹션명")
    page_number: int = Field(..., description="페이지 번호")
    url: List[str] = Field(default_factory=list, description="URL 주소 목록")
    cropped_img_path: Optional[str] = Field(None, description="크롭된 이미지 경로")
    source: str = Field(..., description="원본 파일명")

class RetrievedContext(BaseModel):
    """검색된 컨텍스트"""
    metadata: DocumentMetadata
    page_content: str = Field(..., description="문서 내용")

class SearchContextResponse(BaseModel):
    retrieved_contexts: List[RetrievedContext] = Field(default_factory=list)
