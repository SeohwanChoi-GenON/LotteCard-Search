"""
User ID Value Object
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserIdVO:
    """사용자 고유 식별자"""

    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("User ID cannot be empty")

        if len(self.value) > 50:
            raise ValueError("User ID cannot exceed 50 characters")

    @classmethod
    def from_string(cls, value: str) -> 'UserIdVO':
        """문자열로부터 User ID 생성"""
        return cls(value.strip())

    def __str__(self) -> str:
        return self.value