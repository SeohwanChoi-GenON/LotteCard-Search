"""
Message Role Value Object
"""

from dataclasses import dataclass
from enum import Enum


class MessageRole(Enum):
    """메시지 역할"""
    USER = "user"
    ASSISTANT = "assistant"
    FILE = "file"
    SYSTEM = "system"


@dataclass(frozen=True)
class MessageRoleVO:
    """메시지 역할 Value Object"""

    value: MessageRole

    @classmethod
    def user(cls) -> 'MessageRoleVO':
        """사용자 메시지 역할"""
        return cls(MessageRole.USER)

    @classmethod
    def assistant(cls) -> 'MessageRoleVO':
        """어시스턴트 메시지 역할"""
        return cls(MessageRole.ASSISTANT)

    @classmethod
    def file(cls) -> 'MessageRoleVO':
        """파일 메시지 역할"""
        return cls(MessageRole.FILE)

    @classmethod
    def system(cls) -> 'MessageRoleVO':
        """시스템 메시지 역할"""
        return cls(MessageRole.SYSTEM)

    @classmethod
    def from_string(cls, role_str: str) -> 'MessageRoleVO':
        """문자열로부터 역할 생성"""
        try:
            role = MessageRole(role_str.lower())
            return cls(role)
        except ValueError:
            raise ValueError(f"Invalid message role: {role_str}")

    @property
    def is_user(self) -> bool:
        """사용자 메시지인지"""
        return self.value == MessageRole.USER

    @property
    def is_assistant(self) -> bool:
        """어시스턴트 메시지인지"""
        return self.value == MessageRole.ASSISTANT

    @property
    def is_file(self) -> bool:
        """파일 메시지인지"""
        return self.value == MessageRole.FILE

    def __str__(self) -> str:
        return self.value.value