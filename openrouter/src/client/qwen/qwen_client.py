# clients/qwen_client.py
from openrouter.src.client.base_client import BaseLLMClient
import httpx
from typing import AsyncIterator, Union


class QwenClient(BaseLLMClient):
    def __init__(self, settings):
        super().__init__(settings)
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {settings.qwen_api_key}",
            "Content-Type": "application/json"
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
        """Qwen Chat API 호출 (Stream 지원)"""

        payload = {
            "model": model or self.settings.qwen_model,
            "input": {
                "messages": messages
            },
            "parameters": {
                "max_tokens": max_tokens or self.settings.max_tokens,
                "temperature": temperature or self.settings.temperature,
                "result_format": "message",
                "incremental_output": stream  # Qwen의 스트림 파라미터
            }
        }

        if stream:
            return self._stream_completion(payload)
        else:
            return await self._regular_completion(payload)

    async def _regular_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """일반 완료 요청"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/services/aigc/text-generation/generation",
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                qwen_response = response.json()
                # Qwen 응답을 OpenAI 형식으로 변환
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": qwen_response["output"]["choices"][0]["message"]["content"]
                        },
                        "finish_reason": qwen_response["output"]["choices"][0]["finish_reason"]
                    }],
                    "usage": qwen_response.get("usage", {}),
                    "model": payload["model"]
                }
            else:
                self._handle_error(response, "Qwen")

    async def _stream_completion(self, payload: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """스트림 완료 요청"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                    "POST",
                    f"{self.base_url}/services/aigc/text-generation/generation",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
            ) as response:

                if response.status_code != 200:
                    self._handle_error(response, "Qwen")

                async for line in response.aiter_lines():
                    if line.strip():
                        parsed_data = self._parse_qwen_stream(line)
                        if parsed_data:
                            yield parsed_data

    def _parse_qwen_stream(self, line: str) -> Optional[Dict[str, Any]]:
        """Qwen 스트림 데이터 파싱"""
        if line.startswith("data:"):
            data = line[5:].strip()  # "data:" 제거
            if data == "[DONE]":
                return None
            try:
                qwen_data = json.loads(data)

                # Qwen 스트림을 OpenAI 형식으로 변환
                if "output" in qwen_data and "choices" in qwen_data["output"]:
                    choice = qwen_data["output"]["choices"][0]
                    content = choice["message"]["content"]
                    finish_reason = choice.get("finish_reason")

                    return {
                        "choices": [{
                            "delta": {
                                "content": content
                            },
                            "finish_reason": finish_reason
                        }]
                    }
                return None
            except json.JSONDecodeError:
                return None
        return None

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Qwen 모델 목록"""
        return [
            {"id": "qwen-max", "object": "model"},
            {"id": "qwen-plus", "object": "model"},
            {"id": "qwen-turbo", "object": "model"}
        ]