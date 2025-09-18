"""라우터 자동 등록 팩토리"""
from typing import List, Optional
from dataclasses import dataclass
from fastapi import APIRouter
import importlib
import logging
import inspect
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RouterConfig:
    """라우터 설정"""
    module_path: str
    router_name: str
    prefix: Optional[str] = None
    tags: Optional[List[str]] = None


class RouterRegistry:
    """라우터 자동 발견 및 등록"""

    def __init__(self):
        self._routers: List[APIRouter] = []
        self._scan_paths = ["infrastructure.adapters.primary.web"]

    def get_routers(self) -> List[APIRouter]:
        """등록된 라우터 반환"""
        return self._routers.copy()

    def setup_all_routers(self) -> None:
        """모든 라우터 설정 (진입점)"""
        self._add_system_routes()
        self._discover_and_register_routers()

    def _add_system_routes(self) -> None:
        """시스템 기본 라우터 추가"""
        system_router = APIRouter(tags=["system"])

        @system_router.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "service": "LOCA Chat API",
                "version": "1.0.0"
            }

        @system_router.get("/")
        async def root():
            return {
                "message": "LOCA Chat API",
                "version": "1.0.0",
                "docs": "/docs"
            }

        self._routers.append(system_router)
        logger.info("System routes added")

    def _discover_and_register_routers(self) -> None:
        """라우터 발견 및 등록"""
        for scan_path in self._scan_paths:
            try:
                routers = self._find_routers_in_path(scan_path)
                self._routers.extend(routers)
                logger.info(f"Found {len(routers)} routers in {scan_path}")
            except Exception as e:
                logger.warning(f"Failed to scan {scan_path}: {e}")

    def _find_routers_in_path(self, module_path: str) -> List[APIRouter]:
        """지정된 경로에서 라우터 찾기"""
        routers = []

        try:
            base_path = Path(__file__).parent.parent.parent
            scan_dir = base_path / module_path.replace('.', '/')

            if not scan_dir.exists():
                logger.debug(f"Path not found: {scan_dir}")
                return routers

            # Python 파일 스캔
            for py_file in scan_dir.rglob("*.py"):
                if py_file.name.startswith("__"):
                    continue

                module_name = self._get_module_name(py_file, base_path)
                found_routers = self._extract_routers_from_module(module_name)
                routers.extend(found_routers)

        except Exception as e:
            logger.error(f"Error scanning {module_path}: {e}")

        return routers

    def _get_module_name(self, file_path: Path, base_path: Path) -> str:
        """파일 경로를 모듈 이름으로 변환"""
        relative_path = file_path.relative_to(base_path)
        return str(relative_path.with_suffix('')).replace('/', '.')

    def _extract_routers_from_module(self, module_name: str) -> List[APIRouter]:
        """모듈에서 APIRouter 인스턴스 추출"""
        routers = []

        try:
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module):
                if isinstance(obj, APIRouter):
                    # prefix와 tags 설정
                    if not obj.prefix:
                        obj.prefix = self._infer_prefix(name, module_name)
                    if not obj.tags:
                        obj.tags = self._infer_tags(name, module_name)

                    routers.append(obj)
                    logger.info(f"Found router: {name} in {module_name}")

        except ImportError:
            logger.debug(f"Could not import {module_name}")
        except Exception as e:
            logger.error(f"Error processing {module_name}: {e}")

        return routers

    def _infer_prefix(self, router_name: str, module_path: str) -> Optional[str]:
        """라우터 이름/경로에서 prefix 추론"""
        # 라우터 이름에서 추론 (chat_router -> /chat)
        if router_name.endswith('_router'):
            return f"/{router_name[:-7]}"  # '_router' 제거

        # 모듈 경로에서 추론
        path_parts = module_path.lower().split('.')
        for part in ['chat', 'suggestion', 'upload']:
            if part in path_parts:
                return f"/{part}"

        return None

    def _infer_tags(self, router_name: str, module_path: str) -> Optional[List[str]]:
        """라우터 이름/경로에서 태그 추론"""
        # 라우터 이름에서 추론
        if router_name.endswith('_router'):
            return [router_name[:-7]]

        # 모듈 경로에서 추론
        path_parts = module_path.lower().split('.')
        for part in ['chat', 'suggestion', 'upload']:
            if part in path_parts:
                return [part]

        return None


# 팩토리 함수 (간단한 인터페이스 제공)
def setup_routers() -> List[APIRouter]:
    """라우터 설정 팩토리 함수"""
    registry = RouterRegistry()
    registry.setup_all_routers()
    return registry.get_routers()