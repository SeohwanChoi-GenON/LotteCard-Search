"""
Message Content Value Object
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class MessageContentVO:
    """메시지 내용 Value Object"""

    content: str
    created_date: datetime
    additional_kwargs: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError("Message content cannot be empty")

        if len(self.content) > 10000:  # 실제 제한에 맞게 조정
            raise ValueError("Message content too long")

        # additional_kwargs가 None이면 빈 dict로 설정
        if self.additional_kwargs is None:
            object.__setattr__(self, 'additional_kwargs', {})

    @classmethod
    def create(
            cls,
            content: str,
            created_date: Optional[datetime] = None,
            additional_kwargs: Optional[Dict[str, Any]] = None
    ) -> 'MessageContentVO':
        """메시지 내용 생성"""
        return cls(
            content=content.strip(),
            created_date=created_date or datetime.now(),
            additional_kwargs=additional_kwargs or {}
        )

    @property
    def has_additional_data(self) -> bool:
        """추가 데이터가 있는지 확인"""
        return bool(self.additional_kwargs)

    @property
    def created_date_iso(self) -> str:
        """ISO 형식의 생성일시"""
        return self.created_date.isoformat()