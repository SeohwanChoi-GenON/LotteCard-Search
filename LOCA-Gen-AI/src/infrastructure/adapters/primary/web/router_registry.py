"""
🎯 Primary Adapter Router Registry

모든 Primary Adapter(컨트롤러)를 자동으로 등록하고 관리합니다.
"""
import importlib
import pkgutil
from typing import Dict, List, Any, Optional, NamedTuple
from dataclasses import dataclass
from fastapi import APIRouter

from configuration import LOCAConfig, DeploymentEnvironment


@dataclass
class ControllerConfig:
    """컨트롤러(Primary Adapter) 설정"""
    name: str
    module_path: str
    router_name: str = "router"
    prefix: str = ""
    tags: Optional[List[str]] = None
    enabled: bool = True
    environments: Optional[List[DeploymentEnvironment]] = None
    description: Optional[str] = None
    version: str = "v1"


class ControllerInfo(NamedTuple):
    """등록된 컨트롤러 정보"""
    name: str
    router: APIRouter
    prefix: str
    tags: List[str]
    config: ControllerConfig


class RouterRegistry:
    """Primary Adapter Router 등록 및 관리"""

    def __init__(self, config: LOCAConfig, container: Any):
        self.config = config
        self.container = container
        self._registered_controllers: List[ControllerInfo] = []
        self._controller_metadata: Dict[str, Dict[str, Any]] = {}

    async def register_all_controllers(self) -> List[ControllerInfo]:
        """모든 Primary Adapter 컨트롤러 등록"""
        print("🔍 Discovering Primary Adapter Controllers...")

        # 컨트롤러 경로에서 스캔
        controllers_path = "infrastructure.adapters.primary.web.controllers"

        discovered_controllers = []
        try:
            controllers = await self._scan_controllers_package(controllers_path)
            discovered_controllers.extend(controllers)

        except ImportError as e:
            if self.config.debug_mode:
                print(f"⚠️ Controllers package {controllers_path} not found: {e}")
        except Exception as e:
            print(f"❌ Error scanning {controllers_path}: {e}")

        # 환경별 필터링
        filtered_controllers = self._filter_controllers_by_environment(discovered_controllers)

        # 등록
        for controller_info in filtered_controllers:
            self._register_controller_info(controller_info)

        print(f"✅ Discovered and registered {len(filtered_controllers)} Primary Adapter controllers")
        return filtered_controllers

    async def _scan_controllers_package(self, package_path: str) -> List[ControllerInfo]:
        """컨트롤러 패키지 스캔"""
        controllers = []

        try:
            # 패키지 임포트
            package = importlib.import_module(package_path)

            # 패키지 내 모든 모듈 스캔
            if hasattr(package, '__path__'):
                for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
                    module_path = f"{package_path}.{modname}"

                    try:
                        controller_info = await self._extract_controller_from_module(module_path)
                        if controller_info:
                            controllers.append(controller_info)

                    except Exception as e:
                        if self.config.debug_mode:
                            print(f"⚠️ Failed to extract controller from {module_path}: {e}")

        except Exception as e:
            if self.config.debug_mode:
                print(f"⚠️ Error scanning package {package_path}: {e}")

        return controllers

    async def _extract_controller_from_module(self, module_path: str) -> Optional[ControllerInfo]:
        """모듈에서 컨트롤러 추출"""
        try:
            module = importlib.import_module(module_path)

            # 라우터 찾기 (우선순위별)
            router_candidates = [
                'router',           # 기본
                'api_router',       # 명시적
                f'{module_path.split(".")[-1]}_router',  # 모듈명_router
            ]

            router = None
            router_name = None

            for candidate in router_candidates:
                if hasattr(module, candidate):
                    attr = getattr(module, candidate)
                    if isinstance(attr, APIRouter):
                        router = attr
                        router_name = candidate
                        break

            if router is None:
                # APIRouter 인스턴스를 직접 찾기
                for attr_name in dir(module):
                    if not attr_name.startswith('_'):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, APIRouter):
                            router = attr
                            router_name = attr_name
                            break

            if router is None:
                return None

            # 컨트롤러 정보 구성
            controller_info = self._build_controller_info(
                module_path=module_path,
                router=router,
                router_name=router_name
            )

            return controller_info

        except Exception as e:
            if self.config.debug_mode:
                print(f"⚠️ Error extracting controller from {module_path}: {e}")
            return None

    def _build_controller_info(self, module_path: str, router: APIRouter, router_name: str) -> ControllerInfo:
        """컨트롤러 정보 구성"""
        # 모듈 경로에서 정보 추출
        path_parts = module_path.split('.')

        # 기본 설정
        name = path_parts[-1].replace('_controller', '')  # _controller 접미사 제거
        prefix = f"/{name}"
        tags = [name]

        # 특별한 경우 처리
        if name == "health":
            prefix = "/health"
            tags = ["health", "monitoring"]
        elif name == "search":
            prefix = "/search"
            tags = ["search", "ai"]
        elif name == "user":
            prefix = "/users"
            tags = ["users", "authentication"]

        # 기존 라우터 설정 우선 적용
        if router.prefix:
            prefix = router.prefix
        if router.tags:
            tags = router.tags

        # ControllerConfig 생성
        config = ControllerConfig(
            name=name,
            module_path=module_path,
            router_name=router_name,
            prefix=prefix,
            tags=tags,
            description=f"Primary Adapter controller for {name}"
        )

        return ControllerInfo(
            name=name,
            router=router,
            prefix=prefix,
            tags=tags,
            config=config
        )

    def _filter_controllers_by_environment(self, controllers: List[ControllerInfo]) -> List[ControllerInfo]:
        """환경별 컨트롤러 필터링"""
        filtered_controllers = []

        for controller_info in controllers:
            if self._should_load_controller(controller_info):
                filtered_controllers.append(controller_info)
            else:
                print(f"⏭️  Skipped {controller_info.name} (not allowed in {self.config.deployment_env.value})")

        return filtered_controllers

    def _should_load_controller(self, controller_info: ControllerInfo) -> bool:
        """환경별 컨트롤러 로드 여부 결정"""
        # 디버그 컨트롤러는 개발/로컬 환경에서만
        if "debug" in controller_info.tags:
            return self.config.environment.enable_debug_endpoints

        # 실험적 기능 컨트롤러
        if "experimental" in controller_info.tags:
            return self.config.environment.enable_experimental_features

        # 관리자 컨트롤러는 운영에서 비활성화
        if "admin" in controller_info.tags and self.config.is_production():
            return False

        return True

    def _register_controller_info(self, controller_info: ControllerInfo):
        """컨트롤러 정보 등록"""
        self._registered_controllers.append(controller_info)

        # 메타데이터 저장
        self._controller_metadata[controller_info.name] = {
            "module_path": controller_info.config.module_path,
            "prefix": controller_info.prefix,
            "tags": controller_info.tags,
            "description": controller_info.config.description,
            "route_count": len(controller_info.router.routes)
        }

    def get_registered_controllers(self) -> List[ControllerInfo]:
        """등록된 컨트롤러 목록 반환"""
        return self._registered_controllers

    def get_registry_info(self) -> Dict[str, Any]:
        """레지스트리 전체 정보 반환"""
        total_routes = sum(
            len(controller_info.router.routes)
            for controller_info in self._registered_controllers
        )

        return {
            "total_controllers": len(self._registered_controllers),
            "total_routes": total_routes,
            "deployment_env": self.config.deployment_env.value,
            "controllers": self._controller_metadata
        }