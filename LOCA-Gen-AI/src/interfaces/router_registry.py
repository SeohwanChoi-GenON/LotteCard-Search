import importlib

from fastapi import APIRouter
from typing import List

from interfaces.config.router_config import ROUTER_CONFIGS


class RouterRegistry:
    def __init__(self):
        self._routers: List[APIRouter] = []

    def register(self, router: APIRouter):
        """라우터 수동 등록"""
        self._routers.append(router)

    def auto_register_from_config(self):
        """설정 파일 기반으로 라우터 자동 등록"""
        for config in ROUTER_CONFIGS:
            if not config.enabled:
                continue

            try:
                # 모듈 임포트
                module = importlib.import_module(config.module_path)

                # 라우터 가져오기
                router = getattr(module, config.router_name)

                if isinstance(router, APIRouter):
                    # 설정 적용 (기존 설정이 없는 경우만)
                    if config.prefix and not router.prefix:
                        router.prefix = config.prefix
                    if config.tags and not router.tags:
                        router.tags = config.tags

                    self.register(router)
                    print(f"Registered router: {config.router_name} from {config.module_path}")
                else:
                    print(f"Warning: {config.router_name} is not an APIRouter instance")

            except ImportError as e:
                print(f"Error importing module {config.module_path}: {e}")
            except AttributeError as e:
                print(f"Error finding router {config.router_name} in {config.module_path}: {e}")
            except Exception as e:
                print(f"Error registering router {config.router_name}: {e}")

    def get_registered_routers(self) -> List[APIRouter]:
        return self._routers
        