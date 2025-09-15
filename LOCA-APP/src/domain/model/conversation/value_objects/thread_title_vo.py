"""
Thread Title Value Object
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TitleType(Enum):
    """제목 타입"""
    USER_GENERATED = "user_generated"    # 사용자가 직접 설정
    AI_GENERATED = "ai_generated"        # AI가 자동 생성
    DEFAULT = "default"                  # 기본값


@dataclass(frozen=True)
class ThreadTitleVO:
    """대화 스레드 제목 Value Object"""

    title: str
    title_type: TitleType

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Thread title cannot be empty")

        if len(self.title) > 200:
            raise ValueError("Thread title cannot exceed 200 characters")

    @classmethod
    def user_generated(cls, title: str) -> 'ThreadTitleVO':
        """사용자가 설정한 제목"""
        return cls(title.strip(), TitleType.USER_GENERATED)

    @classmethod
    def ai_generated(cls, title: str) -> 'ThreadTitleVO':
        """AI가 생성한 제목"""
        return cls(title.strip(), TitleType.AI_GENERATED)

    @classmethod
    def default_title(cls) -> 'ThreadTitleVO':
        """기본 제목"""
        return cls("새로운 대화", TitleType.DEFAULT)

    @property
    def is_user_generated(self) -> bool:
        """사용자가 생성한 제목인지"""
        return self.title_type == TitleType.USER_GENERATED

    @property
    def is_ai_generated(self) -> bool:
        """AI가 생성한 제목인지"""
        return self.title_type == TitleType.AI_GENERATED

    def __str__(self) -> str:
        return self.title