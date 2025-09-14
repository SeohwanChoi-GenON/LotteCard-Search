from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from fastapi import APIRouter
import importlib
import logging
import os
import inspect
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RouterConfig:
    module_path: str
    router_name: str
    prefix: Optional[str] = None
    tags: Optional[List[str]] = None
    enabled: bool = True


class RouterRegistry:
    def __init__(self):
        self._routers: List[APIRouter] = []
        self._base_router_paths = [
            "infrastructure.adapters.primary.web"
        ]

    def register_router(self, router: APIRouter) -> None:
        """라우터 수동 등록"""
        self._routers.append(router)
        logger.info(f"Manually registered router: {router.__class__.__name__}")

    def auto_register_from_configs(self) -> None:
        """자동 라우터 발견 및 등록"""
        # 개발용 기본 라우터 추가
        self._add_basic_routes()

        # 라우터 자동 발견
        discovered_routers = self._discover_routers()

        for router_config in discovered_routers:
            try:
                self._register_router_from_config(router_config)
            except Exception as e:
                logger.error(f"Failed to register router {router_config.router_name}: {e}")

    def _add_basic_routes(self):
        """개발용 기본 라우터 - 최소한의 엔드포인트"""
        basic_router = APIRouter(tags=["system"])

        @basic_router.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "LOCA Chat API", "version": "1.0.0"}

        @basic_router.get("/")
        async def root():
            return {
                "message": "LOCA Chat API",
                "version": "1.0.0",
                "docs": "/docs",
                "health": "/api/v1/health"
            }

        self.register_router(basic_router)

    def _discover_routers(self) -> List[RouterConfig]:
        """라우터 자동 발견"""
        discovered = []

        for base_path in self._base_router_paths:
            try:
                configs = self._scan_module_for_routers(base_path)
                discovered.extend(configs)
            except ImportError as e:
                logger.info(f"Module not found, skipping: {base_path} ({e})")
            except Exception as e:
                logger.error(f"Error scanning module {base_path}: {e}")

        return discovered

    def _scan_module_for_routers(self, module_path: str) -> List[RouterConfig]:
        """특정 모듈에서 APIRouter 인스턴스들을 찾아서 RouterConfig 생성"""
        configs = []

        try:
            # 모듈의 실제 파일 경로 확인
            src_path = Path(__file__).parent.parent.parent
            module_file_path = src_path / module_path.replace('.', '/')

            if not module_file_path.exists():
                logger.debug(f"Module path does not exist: {module_file_path}")
                return configs

            # Python 파일들 스캔
            for py_file in module_file_path.rglob("*.py"):
                if py_file.name == "__init__.py":
                    continue

                # 모듈 경로 구성
                relative_path = py_file.relative_to(src_path)
                module_name = str(relative_path.with_suffix('')).replace(os.sep, '.')

                try:
                    module = importlib.import_module(module_name)
                    router_configs = self._extract_routers_from_module(module, module_name)
                    configs.extend(router_configs)
                except Exception as e:
                    logger.debug(f"Could not import module {module_name}: {e}")

        except Exception as e:
            logger.error(f"Error scanning module {module_path}: {e}")

        return configs

    def _extract_routers_from_module(self, module, module_path: str) -> List[RouterConfig]:
        """모듈에서 APIRouter 인스턴스들을 추출"""
        configs = []

        for name, obj in inspect.getmembers(module):
            if isinstance(obj, APIRouter):
                # 라우터 이름과 태그로부터 prefix 추론
                prefix = self._infer_prefix_from_router(obj, name, module_path)
                tags = self._infer_tags_from_router(obj, name, module_path)

                config = RouterConfig(
                    module_path=module_path,
                    router_name=name,
                    prefix=prefix,
                    tags=tags,
                    enabled=True
                )
                configs.append(config)
                logger.info(f"Discovered router: {name} in {module_path}")

        return configs

    def _infer_prefix_from_router(self, router: APIRouter, name: str, module_path: str) -> Optional[str]:
        """라우터 이름이나 모듈 경로에서 prefix 추론"""
        # 이미 prefix가 설정되어 있으면 그것을 사용
        if hasattr(router, 'prefix') and router.prefix:
            return router.prefix

        # 라우터 이름에서 추론 (chat_router -> /chat)
        if name.endswith('_router'):
            return f"/{name.replace('_router', '')}"

        # 모듈 경로에서 추론 (chat_controller -> /chat)
        if 'chat' in module_path.lower():
            return '/chat'
        elif 'user' in module_path.lower():
            return '/users'
        elif 'auth' in module_path.lower():
            return '/auth'

        return None

    def _infer_tags_from_router(self, router: APIRouter, name: str, module_path: str) -> Optional[List[str]]:
        """라우터에서 태그 추론"""
        # 이미 태그가 설정되어 있으면 그것을 사용
        if hasattr(router, 'tags') and router.tags:
            return router.tags

        # 라우터 이름에서 추론
        if name.endswith('_router'):
            tag = name.replace('_router', '')
            return [tag]

        # 모듈 경로에서 추론
        if 'chat' in module_path.lower():
            return ['chat']
        elif 'user' in module_path.lower():
            return ['users']
        elif 'auth' in module_path.lower():
            return ['auth']

        return None

    def _register_router_from_config(self, config: RouterConfig) -> None:
        """개별 라우터 설정으로부터 등록"""
        module = importlib.import_module(config.module_path)
        router = getattr(module, config.router_name)

        if not isinstance(router, APIRouter):
            raise ValueError(f"{config.router_name} is not an APIRouter instance")

        # 설정 적용 (기존 설정이 없는 경우만)
        if config.prefix and not getattr(router, 'prefix', None):
            router.prefix = config.prefix
        if config.tags and not getattr(router, 'tags', None):
            router.tags = config.tags

        self._routers.append(router)
        logger.info(f"Auto-registered router: {config.router_name} from {config.module_path}")

    def get_routers(self) -> List[APIRouter]:
        """등록된 모든 라우터 반환"""
        return self._routers.copy()

    def add_router_config(self, config: RouterConfig) -> None:
        """런타임에 라우터 설정 추가"""
        try:
            self._register_router_from_config(config)
        except Exception as e:
            logger.error(f"Failed to add router config {config.router_name}: {e}")

    def add_router_path(self, base_path: str) -> None:
        """새로운 스캔 경로 추가"""
        if base_path not in self._base_router_paths:
            self._base_router_paths.append(base_path)
            logger.info(f"Added router scan path: {base_path}")