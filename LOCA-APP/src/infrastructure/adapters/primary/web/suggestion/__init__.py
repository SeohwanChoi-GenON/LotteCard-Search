"""
Suggestion 어댑터 모듈

연관질문 생성 관련 웹 어댑터를 제공합니다.
"""

from .suggestion_controller import suggestion_router

__all__ = ["suggestion_router"]