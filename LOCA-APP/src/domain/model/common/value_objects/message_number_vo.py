"""
Message Number Value Object
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MessageNumberVO:
    """메시지 순서 번호"""

    value: int

    def __post_init__(self):
        if self.value < 1:
            raise ValueError("Message number must be positive")

    @classmethod
    def first(cls) -> 'MessageNumberVO':
        """첫 번째 메시지 번호"""
        return cls(1)

    @classmethod
    def next_from(cls, current: 'MessageNumberVO') -> 'MessageNumberVO':
        """다음 메시지 번호 생성"""
        return cls(current.value + 1)

    def __str__(self) -> str:
        return str(self.value)