from client.base_client import BaseLLMClient
import httpx
from typing import AsyncIterator, Union, Dict, Any, List, Optional


class OpenRouterClient(BaseLLMClient):
    def __init__(self, settings):
        super().__init__(settings)
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Multi-LLM Client"
        }

    async def chat_completion(
            self,
            messages: List[Dict[str, str]],
            model: Optional[str] = None,
            max_tokens: Optional[int] = None,
            temperature: Optional[float] = None,
            stream: bool = False,
            **kwargs
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """OpenRouter Chat Completion API 호출 (Stream 지원)"""

        payload = {
            "model": model or self.settings.openrouter_model,
            "messages": messages,
            "max_tokens": max_tokens or self.settings.max_tokens,
            "temperature": temperature or self.settings.temperature,
            "stream": stream
        }

        if "top_p" in kwargs:
            payload["top_p"] = kwargs["top_p"]
        if "top_k" in kwargs:
            payload["top_k"] = kwargs["top_k"]
        if "repetition_penalty" in kwargs:
            payload["repetition_penalty"] = kwargs["repetition_penalty"]

        if stream:
            return self._stream_completion(payload)
        else:
            return await self._regular_completion(payload)

    async def _regular_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """일반 완료 요청"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 402:
                raise Exception("OpenRouter: 크레딧이 부족합니다.")
            elif response.status_code == 429:
                raise Exception("OpenRouter: 요청 한도 초과")
            else:
                raise Exception(f"OpenRouter API 호출 실패: {response.status_code} - {response.text}")


    async def _stream_completion(self, payload: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """스트림 완료 요청"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                    "POST",
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
            ) as response:

                if response.status_code != 200:
                    self._handle_error(response, "OpenRouter")

                async for line in response.aiter_lines():
                    if line.strip():
                        parsed_data = self._parse_sse_line(line)
                        if parsed_data:
                            yield parsed_data

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """OpenRouter 모델 목록 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/models",
                headers=self.headers
            )

            if response.status_code == 200:
                return response.json()["data"]
            else:
                self._handle_error(response, "OpenRouter")