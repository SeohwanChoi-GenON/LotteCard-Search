"""
웹 어댑터 공통 검증 로직

모든 웹 어댑터에서 공통으로 사용하는 검증 함수들을 정의합니다.
"""

import re
from typing import Optional
from infrastructure.adapters.primary.web.common.schemas.base_schemas import ServiceId


def validate_thread_id(thread_id: str) -> str:
    """Thread ID 검증"""
    if not thread_id:
        raise ValueError("thread_id는 필수입니다.")

    if len(thread_id) > 50:
        raise ValueError("thread_id는 50자를 초과할 수 없습니다.")

    # 영문, 숫자, 언더스코어, 하이픈만 허용
    if not re.match(r'^[a-zA-Z0-9_-]+$', thread_id):
        raise ValueError("thread_id는 영문, 숫자, 언더스코어, 하이픈만 포함할 수 있습니다.")

    return thread_id


def validate_user_id(user_id: str) -> str:
    """User ID 검증"""
    if not user_id:
        raise ValueError("user_id는 필수입니다.")

    if len(user_id) > 20:
        raise ValueError("user_id는 20자를 초과할 수 없습니다.")

    # 영문, 숫자, 언더스코어만 허용
    if not re.match(r'^[a-zA-Z0-9_]+$', user_id):
        raise ValueError("user_id는 영문, 숫자, 언더스코어만 포함할 수 있습니다.")

    return user_id


def validate_service_id(service_id: str) -> ServiceId:
    """Service ID 검증"""
    try:
        return ServiceId(service_id)
    except ValueError:
        valid_services = [service.value for service in ServiceId]
        raise ValueError(f"service_id는 {valid_services} 중 하나여야 합니다.")


def validate_user_input(user_input: str, max_length: int = 1000) -> str:
    """사용자 입력 텍스트 검증"""
    if not user_input:
        raise ValueError("user_input은 필수입니다.")

    user_input = user_input.strip()
    if not user_input:
        raise ValueError("user_input은 공백만으로 구성될 수 없습니다.")

    if len(user_input) > max_length:
        raise ValueError(f"user_input은 {max_length}자를 초과할 수 없습니다.")

    return user_input


def validate_message_id(message_id: Optional[int]) -> Optional[int]:
    """Message ID 검증"""
    if message_id is None:
        return None

    if message_id < 1:
        raise ValueError("message_id는 1 이상이어야 합니다.")

    return message_id