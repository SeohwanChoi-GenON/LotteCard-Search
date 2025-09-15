"""
Service ID Value Object
"""

from dataclasses import dataclass
from enum import Enum


class ServiceType(Enum):
    """지원되는 서비스 타입"""
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"


@dataclass(frozen=True)
class ServiceIdVO:
    """서비스 고유 식별자"""

    value: ServiceType

    @classmethod
    def from_string(cls, value: str) -> 'ServiceIdVO':
        """문자열로부터 Service ID 생성"""
        try:
            service_type = ServiceType(value)
            return cls(service_type)
        except ValueError:
            raise ValueError(f"Invalid service type: {value}. Valid types: {[t.value for t in ServiceType]}")

    def __str__(self) -> str:
        return self.value.value

    @property
    def is_unified(self) -> bool:
        """통합 서비스 여부"""
        return self.value == ServiceType.UNIFIED

    @property
    def requires_specific_search(self) -> bool:
        """특정 검색이 필요한 서비스인지"""
        return self.value in [ServiceType.CARD, ServiceType.EVENT, ServiceType.CONTENTS]