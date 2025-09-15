"""
메시지 Entity (대화 히스토리 API 규격 기반)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from ...common.value_objects.thread_id_vo import ThreadIdVO
from ...common.value_objects.message_number_vo import MessageNumberVO
from ..value_objects.message_role_vo import MessageRoleVO, MessageRole
from ..value_objects.message_content_vo import MessageContentVO


@dataclass
class MessageEntity:
    """대화 메시지 Entity"""

    thread_id: ThreadIdVO
    msg_no: MessageNumberVO
    role: MessageRoleVO
    content: MessageContentVO

    def __post_init__(self):
        # 비즈니스 규칙 검증
        if self.role.is_user and not self.content.content.strip():
            raise ValueError("User message content cannot be empty")

    def __eq__(self, other) -> bool:
        """메시지 고유성 비교 (thread_id + msg_no)"""
        if not isinstance(other, MessageEntity):
            return False
        return self.thread_id == other.thread_id and self.msg_no == other.msg_no

    def __hash__(self) -> int:
        """해시 값"""
        return hash((self.thread_id, self.msg_no))

    @classmethod
    def create_user_message(
            cls,
            thread_id: ThreadIdVO,
            msg_no: MessageNumberVO,
            content: str,
            created_date: Optional[datetime] = None,
            additional_kwargs: Optional[Dict[str, Any]] = None
    ) -> 'MessageEntity':
        """사용자 메시지 생성"""
        return cls(
            thread_id=thread_id,
            msg_no=msg_no,
            role=MessageRoleVO.user(),
            content=MessageContentVO.create(content, created_date, additional_kwargs)
        )

    @classmethod
    def create_assistant_message(
            cls,
            thread_id: ThreadIdVO,
            msg_no: MessageNumberVO,
            content: str,
            created_date: Optional[datetime] = None,
            additional_kwargs: Optional[Dict[str, Any]] = None
    ) -> 'MessageEntity':
        """어시스턴트 메시지 생성"""
        return cls(
            thread_id=thread_id,
            msg_no=msg_no,
            role=MessageRoleVO.assistant(),
            content=MessageContentVO.create(content, created_date, additional_kwargs)
        )

    @classmethod
    def create_file_message(
            cls,
            thread_id: ThreadIdVO,
            msg_no: MessageNumberVO,
            content: str,
            created_date: Optional[datetime] = None,
            additional_kwargs: Optional[Dict[str, Any]] = None
    ) -> 'MessageEntity':
        """파일 메시지 생성"""
        return cls(
            thread_id=thread_id,
            msg_no=msg_no,
            role=MessageRoleVO.file(),
            content=MessageContentVO.create(content, created_date, additional_kwargs)
        )

    @property
    def is_user_message(self) -> bool:
        """사용자 메시지인지"""
        return self.role.is_user

    @property
    def is_assistant_message(self) -> bool:
        """어시스턴트 메시지인지"""
        return self.role.is_assistant

    @property
    def is_file_message(self) -> bool:
        """파일 메시지인지"""
        return self.role.is_file

    def to_api_format(self) -> Dict[str, Any]:
        """API 형식으로 변환 (대화 히스토리 저장용)"""
        return {
            "role": str(self.role),
            "content": self.content.content,
            "additional_kwargs": self.content.additional_kwargs,
            "created_date": self.content.created_date_iso,
            "msg_no": self.msg_no.value
        }