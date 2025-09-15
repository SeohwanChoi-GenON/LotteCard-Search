"""
서비스 관련 타입 정의

서비스 ID와 관련된 Enum을 정의합니다.
"""
from enum import Enum


class ServiceId(str, Enum):
    """서비스 식별자"""
    UNIFIED = "Unified"
    CARD = "Card"
    EVENT = "Event"
    CONTENTS = "Contents"
    COMMERCE = "Commerce"
    MENU = "Menu"