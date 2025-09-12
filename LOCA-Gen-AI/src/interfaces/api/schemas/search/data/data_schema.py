from typing import Optional

from pydantic import BaseModel, Field


class GeneralAnswerTemplate(BaseModel):
    """답변 템플릿"""
    template_type: str = Field(..., description="템플릿 타입")
    template_contents: str = Field(..., description="템플릿 내용")

class SearchDataResponse(BaseModel):
    """챗봇 데이터 응답"""
    general_answer: str = Field(..., max_length=5000, description="AI 생성 답변")
    general_answer_template: Optional[GeneralAnswerTemplate] = Field(None, description="템플릿 답변 구조")
