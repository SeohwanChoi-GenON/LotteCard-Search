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
