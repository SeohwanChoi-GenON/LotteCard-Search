from typing import Optional

from pydantic import BaseModel


class RouterConfig(BaseModel):
    module_path: str
    router_name: str
    prefix: Optional[str] = None
    tags: Optional[list[str]] = None
    enabled:bool = True

# 라우터 설정 목록
ROUTER_CONFIGS = [
    RouterConfig(
        module_path="interfaces.api.v1.chat.chat_controller",
        router_name="chat_router",
        prefix="/chat",
        tags=["chat"],
        enabled=True
    )
]