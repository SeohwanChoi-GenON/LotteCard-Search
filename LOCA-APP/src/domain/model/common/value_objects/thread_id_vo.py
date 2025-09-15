"""
Thread ID Value Object
"""

from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class ThreadIdVO:
    """대화 스레드 고유 식별자"""

    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Thread ID cannot be empty")

        if len(self.value) > 100:
            raise ValueError("Thread ID cannot exceed 100 characters")

    @classmethod
    def generate(cls) -> 'ThreadIdVO':
        """새로운 Thread ID 생성"""
        return cls(str(uuid.uuid4()))

    @classmethod
    def from_string(cls, value: str) -> 'ThreadIdVO':
        """문자열로부터 Thread ID 생성"""
        return cls(value.strip())

    def __str__(self) -> str:
        return self.value