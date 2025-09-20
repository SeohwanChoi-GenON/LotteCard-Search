# clients/base_client.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator, Union
import httpx
import json


class BaseLLMClient(ABC):
    def __init__(self, settings):
        self.settings = settings
        self.timeout = 30.0

    @abstractmethod
    async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: Optional[str] = None,
            max_tokens: Optional[int] = None,
            temperature: Optional[float] = None,
            stream: bool = False,
            **kwargs
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        pass

    @abstractmethod
    async def get_available_models(self) -> List[Dict[str, Any]]:
        pass

    def _handle_error(self, response: httpx.Response, provider: str):
        """공통 에러 처리"""
        if response.status_code == 401:
            raise Exception(f"{provider}: 인증 실패 - API 키를 확인하세요")
        elif response.status_code == 402:
            raise Exception(f"{provider}: 크레딧이 부족합니다")
        elif response.status_code == 429:
            raise Exception(f"{provider}: 요청 한도 초과")
        else:
            raise Exception(f"{provider}: API 호출 실패 ({response.status_code}) - {response.text}")

    def _parse_sse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Server-Sent Events 라인 파싱"""
        if line.startswith("data: "):
            data = line[6:]  # "data: " 제거
            if data.strip() == "[DONE]":
                return None
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None