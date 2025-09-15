"""
Thread Aggregate Root (대화 히스토리 관리)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from ...common.value_objects.thread_id_vo import ThreadIdVO
from ...common.value_objects.user_id_vo import UserIdVO
from ...common.value_objects.service_id_vo import ServiceIdVO
from ...common.value_objects.message_number_vo import MessageNumberVO
from ..entities.message_entity import MessageEntity
from ..value_objects.thread_title_vo import ThreadTitleVO, TitleType


class ThreadStatus(Enum):
    """스레드 상태"""
    ACTIVE = "active"
    DELETED = "deleted"


@dataclass
class ThreadAggregate:
    """대화 스레드 Aggregate Root"""

    id: ThreadIdVO
    user_id: UserIdVO
    service_id: ServiceIdVO
    created_at: datetime
    updated_at: datetime
    status: ThreadStatus = ThreadStatus.ACTIVE
    title: Optional[ThreadTitleVO] = None
    _messages: List[MessageEntity] = field(default_factory=list, init=False)
    _is_first_turn_saved: bool = field(default=False, init=False)

    def __eq__(self, other) -> bool:
        """ID 기반 동등성 비교"""
        if not isinstance(other, ThreadAggregate):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """ID 기반 해시"""
        return hash(self.id)

    @classmethod
    def create(
            cls,
            user_id: UserIdVO,
            service_id: ServiceIdVO,
            thread_id: Optional[ThreadIdVO] = None,
            title: Optional[ThreadTitleVO] = None
    ) -> 'ThreadAggregate':
        """새로운 스레드 생성"""
        now = datetime.now()
        return cls(
            id=thread_id or ThreadIdVO.generate(),
            user_id=user_id,
            service_id=service_id,
            created_at=now,
            updated_at=now,
            title=title
        )

    def add_messages_for_first_turn(
            self,
            messages: List[Dict[str, Any]],
            title: Optional[str] = None
    ) -> List[MessageEntity]:
        """첫 턴 메시지 추가 (AIG-LOCA-001)"""
        if self._is_first_turn_saved:
            raise ValueError("First turn already saved for this thread")

        if not messages:
            raise ValueError("Messages cannot be empty for first turn")

        added_messages = []

        for msg_data in messages:
            message = self._create_message_from_data(msg_data)
            self._messages.append(message)
            added_messages.append(message)

        # 제목 설정 (첫 턴에서만)
        if title:
            self.title = ThreadTitleVO.ai_generated(title)
        elif not self.title:
            self.title = ThreadTitleVO.default_title()

        # 생성시각을 첫 턴의 user 메시지 기준으로 설정
        first_user_msg = next(
            (msg for msg in added_messages if msg.is_user_message),
            None
        )
        if first_user_msg:
            self.created_at = first_user_msg.content.created_date

        self._is_first_turn_saved = True
        self.updated_at = datetime.now()

        return added_messages

    def add_messages_for_subsequent_turn(
            self,
            messages: List[Dict[str, Any]]
    ) -> List[MessageEntity]:
        """후속 턴 메시지 추가 (AIG-LOCA-002)"""
        if not self._is_first_turn_saved:
            raise ValueError("First turn must be saved before subsequent turns")

        if not messages:
            raise ValueError("Messages cannot be empty")

        added_messages = []

        for msg_data in messages:
            message = self._create_message_from_data(msg_data)
            self._messages.append(message)
            added_messages.append(message)

        self.updated_at = datetime.now()
        return added_messages

    def update_title(self, title: str, is_user_generated: bool = True) -> None:
        """제목 변경 (AIG-LOCA-003)"""
        if not self._is_first_turn_saved:
            raise ValueError("Cannot update title before first turn is saved")

        self.title = (
            ThreadTitleVO.user_generated(title)
            if is_user_generated
            else ThreadTitleVO.ai_generated(title)
        )
        self.updated_at = datetime.now()

    def mark_as_deleted(self) -> None:
        """대화 삭제 표시 (AIG-LOCA-004)"""
        self.status = ThreadStatus.DELETED
        self.updated_at = datetime.now()

    def _create_message_from_data(self, msg_data: Dict[str, Any]) -> MessageEntity:
        """메시지 데이터로부터 MessageEntity 생성"""
        from ..value_objects.message_role_vo import MessageRoleVO
        from ..value_objects.message_content_vo import MessageContentVO

        role = MessageRoleVO.from_string(msg_data["role"])
        msg_no = MessageNumberVO(msg_data["msg_no"])

        # created_date 파싱
        created_date = datetime.fromisoformat(
            msg_data["created_date"].replace("Z", "+00:00")
        )

        content = MessageContentVO.create(
            content=msg_data["content"],
            created_date=created_date,
            additional_kwargs=msg_data.get("additional_kwargs", {})
        )

        return MessageEntity(
            thread_id=self.id,
            msg_no=msg_no,
            role=role,
            content=content
        )

    @property
    def messages(self) -> tuple[MessageEntity, ...]:
        """메시지 목록 반환 (불변)"""
        return tuple(sorted(self._messages, key=lambda m: m.msg_no.value))

    @property
    def message_count(self) -> int:
        """메시지 개수"""
        return len(self._messages)

    @property
    def is_active(self) -> bool:
        """활성 상태인지"""
        return self.status == ThreadStatus.ACTIVE

    @property
    def is_deleted(self) -> bool:
        """삭제 상태인지"""
        return self.status == ThreadStatus.DELETED

    @property
    def has_title(self) -> bool:
        """제목이 있는지"""
        return self.title is not None

    @property
    def display_title(self) -> str:
        """표시용 제목"""
        return str(self.title) if self.title else "제목 없음"

    def to_api_messages_format(self) -> List[Dict[str, Any]]:
        """API 메시지 형식으로 변환"""
        return [msg.to_api_format() for msg in self.messages]

    def get_context_messages(self, max_messages: int = 10) -> List[MessageEntity]:
        """컨텍스트용 최근 메시지들"""
        sorted_messages = sorted(self._messages, key=lambda m: m.msg_no.value)
        return sorted_messages[-max_messages:] if max_messages > 0 else sorted_messages