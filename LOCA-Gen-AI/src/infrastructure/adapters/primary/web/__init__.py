"""
🌐 Web Framework Primary Adapter

FastAPI 기반의 웹 프레임워크 Primary Adapter입니다.
헥사고날 아키텍처에서 외부 HTTP 요청을 애플리케이션 코어로 전달하는 역할을 합니다.

Primary Adapter의 역할:
- 외부 HTTP 요청을 수신
- 요청을 도메인 Command/Query로 변환
- Primary Port(Use Case)를 통해 애플리케이션 코어 호출
- 응답을 HTTP 형태로 변환하여 반환
- 프레임워크별 횡단 관심사 처리

구성 요소:
- app_factory: FastAPI 애플리케이션 생성 및 구성
- controllers/: HTTP 컨트롤러들 (실제 Primary Adapter 구현)
- schemas/: FastAPI용 요청/응답 스키마들
- middleware/: 횡단 관심사 미들웨어들
- startup/: 애플리케이션 초기화 로직
"""

from .app_factory import create_app, WebApplicationFactory
from .router_registry import RouterRegistry

__version__ = "2.0.0"
__all__ = [
    "create_app",
    "WebApplicationFactory",
    "RouterRegistry",
]

# Web Adapter 메타데이터
WEB_ADAPTER_INFO = {
    "name": "FastAPI Web Framework Primary Adapter",
    "version": __version__,
    "description": "Primary adapter for HTTP requests using FastAPI",
    "framework": "FastAPI",
    "type": "primary_adapter",
    "layer": "infrastructure",
    "ports_used": [
        "application.ports.primary.*",  # Use Cases (Primary Ports)
    ]
}