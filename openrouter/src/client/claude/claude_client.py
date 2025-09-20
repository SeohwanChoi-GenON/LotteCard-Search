# clients/claude_client.py
import json

from openrouter.src.client.base_client import BaseLLMClient
import httpx
from typing import AsyncIterator, Union, List, Dict, Any, Optional


class ClaudeClient(BaseLLMClient):
    def __init__(self, settings):
        super().__init__(settings)
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": settings.claude_api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
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
        """Claude Messages API 호출 (Stream 지원)"""

        # Claude는 system 메시지를 별도로 처리
        system_message = None
        formatted_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                formatted_messages.append(msg)

        payload = {
            "model": model or self.settings.claude_model,
            "messages": formatted_messages,
            "max_tokens": max_tokens or self.settings.max_tokens,
            "stream": stream
        }

        if system_message:
            payload["system"] = system_message
        if temperature is not None:
            payload["temperature"] = temperature or self.settings.temperature

        if stream:
            return self._stream_completion(payload)
        else:
            return await self._regular_completion(payload)

    async def _regular_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """일반 완료 요청"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                # Claude 응답을 OpenAI 형식으로 변환
                claude_response = response.json()
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": claude_response["content"][0]["text"]
                        },
                        "finish_reason": claude_response["stop_reason"]
                    }],
                    "usage": claude_response.get("usage", {}),
                    "model": claude_response["model"]
                }
            else:
                self._handle_error(response, "Claude")

    async def _stream_completion(self, payload: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """스트림 완료 요청"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                    "POST",
                    f"{self.base_url}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
            ) as response:

                if response.status_code != 200:
                    self._handle_error(response, "Claude")

                async for line in response.aiter_lines():
                    if line.strip():
                        parsed_data = self._parse_claude_stream(line)
                        if parsed_data:
                            yield parsed_data

    def _parse_claude_stream(self, line: str) -> Optional[Dict[str, Any]]:
        """Claude 스트림 데이터 파싱"""
        if line.startswith("data: "):
            data = line[6:]
            try:
                claude_data = json.loads(data)

                # Claude 스트림을 OpenAI 형식으로 변환
                if claude_data.get("type") == "content_block_delta":
                    return {
                        "choices": [{
                            "delta": {
                                "content": claude_data["delta"]["text"]
                            },
                            "finish_reason": None
                        }]
                    }
                elif claude_data.get("type") == "message_stop":
                    return {
                        "choices": [{
                            "delta": {},
                            "finish_reason": "stop"
                        }]
                    }
                return None
            except json.JSONDecodeError:
                return None
        return None

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Claude는 고정된 모델 목록 반환"""
        return [
            {"id": "claude-3-opus-20240229", "object": "model"},
            {"id": "claude-3-sonnet-20240229", "object": "model"},
            {"id": "claude-3-haiku-20240307", "object": "model"}
        ]
