# clients/client_factory.py
from enum import Enum
from typing import Dict, Type
from .base_client import BaseLLMClient
from openrouter.src.client.openai.openai_client import OpenAIClient
from openrouter.src.client.claude.claude_client import ClaudeClient
from openrouter.src.client.qwen.qwen_client import QwenClient
from openrouter.src.client.openrouter.openrouter_client import OpenRouterClient


class ModelProvider(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    QWEN = "qwen"
    OPENROUTER = "openrouter"


class LLMClientFactory:
    _clients: Dict[ModelProvider, Type[BaseLLMClient]] = {
        ModelProvider.OPENAI: OpenAIClient,
        ModelProvider.CLAUDE: ClaudeClient,
        ModelProvider.QWEN: QwenClient,
        ModelProvider.OPENROUTER: OpenRouterClient,
    }

    @classmethod
    def create_client(cls, provider: ModelProvider, settings) -> BaseLLMClient:
        """클라이언트 팩토리 메서드"""
        client_class = cls._clients.get(provider)
        if not client_class:
            raise ValueError(f"**지원하지 않는 제공자**: {provider}")
        return client_class(settings)

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """사용 가능한 제공자 목록"""
        return [provider.value for provider in ModelProvider]