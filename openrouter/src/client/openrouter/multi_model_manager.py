from typing import List, Dict, Any, AsyncIterator, Union
import asyncio

from client.openrouter.model_list import OpenRouterModels
from client.openrouter.openrouter_client import OpenRouterClient


class MultiModelManager:
    """여러 모델을 효율적으로 관리하는 매니저"""

    def __init__(self, settings):
        self.client = OpenRouterClient(settings)
        self.models = OpenRouterModels()

    async def chat_with_model(
            self,
            model_name: str,
            messages: List[Dict[str, str]],
            stream: bool = False,
            **kwargs
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """특정 모델로 채팅"""

        all_models = self.models.get_all_models()

        if model_name in all_models:
            model_id = all_models[model_name]
        else:
            model_id = model_name  # 직접 모델 ID 사용

        return await self.client.chat_completion(
            messages=messages,
            model=model_id,
            stream=stream,
            **kwargs
        )

    async def compare_models(
            self,
            model_names: List[str],
            messages: List[Dict[str, str]],
            **kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """여러 모델의 응답 비교 (Non-Stream)"""

        tasks = []
        for model_name in model_names:
            task = self.chat_with_model(
                model_name=model_name,
                messages=messages,
                stream=False,
                **kwargs
            )
            tasks.append((model_name, task))

        results = {}
        responses = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)

        for (model_name, _), response in zip(tasks, responses):
            if isinstance(response, Exception):
                results[model_name] = {"error": str(response)}
            else:
                results[model_name] = {
                    "response": response["choices"][0]["message"]["content"],
                    "usage": response.get("usage", {}),
                    "model": response.get("model", model_name)
                }

        return results

    async def stream_multiple_models(
            self,
            model_names: List[str],
            messages: List[Dict[str, str]],
            **kwargs
    ):
        """여러 모델의 스트림 응답을 동시에 처리"""

        async def stream_single_model(model_name: str):
            try:
                stream_response = await self.chat_with_model(
                    model_name=model_name,
                    messages=messages,
                    stream=True,
                    **kwargs
                )

                print(f"\n=== **{model_name} 스트림 시작** ===")
                content = ""

                async for chunk in stream_response:
                    if "choices" in chunk and chunk["choices"]:
                        delta = chunk["choices"][0].get("delta", {})
                        if "content" in delta:
                            chunk_content = delta["content"]
                            print(f"[{model_name}] {chunk_content}", end="", flush=True)
                            content += chunk_content

                        finish_reason = chunk["choices"][0].get("finish_reason")
                        if finish_reason:
                            print(f"\n[{model_name}] **완료**: {finish_reason}")
                            break

                return model_name, content

            except Exception as e:
                print(f"[{model_name}] **오류**: {e}")
                return model_name, None

        # 모든 모델 동시 스트림
        tasks = [stream_single_model(name) for name in model_names]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def get_available_models_by_provider(self, provider: str) -> List[Dict[str, Any]]:
        """제공자별 사용 가능한 모델 조회"""
        all_models = await self.client.get_available_models()
        return [model for model in all_models if provider.lower() in model["id"].lower()]