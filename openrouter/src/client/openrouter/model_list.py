# models/openrouter_models.py
from typing import Dict, List


class OpenRouterModels:
    """OpenRouter에서 지원하는 주요 모델들"""

    # **OpenAI 모델들**
    GPT_4_1_MINI = "openai/gpt-4.1-mini"
    GPT_5 = "openai/gpt-5"
    GPT_OSS = "openai/gpt-oss-120b"

    # **Anthropic Claude 모델들**
    CLAUDE_4_1_OPUS = "anthropic/claude-opus-4.1"
    CLAUDE_4_SONNET = "anthropic/claude-sonnet-4"

    # **Alibaba Qwen 모델들**
    QWEN3_235B = "qwen/qwen3-235b-a22b-2507"
    QWEN3_30B = "qwen/qwen3-30b-a3b"
    QWEN3_NEXT_80B = "qwen/qwen3-next-80b-a3b-instruct"
    QWEN3_CODER_480B = "qwen/qwen3-coder"

    # **Meta Llama 모델들**
    LLAMA_3_3_70B = "meta-llama/llama-3.3-70b-instruct"
    LLAMA_4_MAVERICK = "meta-llama/llama-4-maverick"

    # **Google 모델들**
    GEMINI_2_5_FLASH = "google/gemini-2.5-flash"
    GEMINI_2_5_PRO = "google/gemini-2.5-pro"

    # **Mistral 모델들**
    MISTRAL_7B = "mistralai/mistral-7b-instruct"
    MIXTRAL_8X7B = "mistralai/mixtral-8x7b-instruct"

    # **Perplexity**
    PERPLEXITY_SONAR_DEEP_SEARCH = "perplexity/sonar-deep-research"
    PERPLEXITY_SONAR = "perplexity/sonar"

    @classmethod
    def get_all_models(cls) -> Dict[str, str]:
        """모든 모델 목록 반환"""
        return {
            # OpenAI
            "gpt-4.1-mini": cls.GPT_4_1_MINI,
            "gpt-5": cls.GPT_5,
            "gpt-oss": cls.GPT_OSS,

            # Claude
            "claude-4.1-opus": cls.CLAUDE_4_1_OPUS,
            "claude-4-sonnet": cls.CLAUDE_4_SONNET,

            # Qwen
            "qwen3-235b": cls.QWEN3_235B,
            "qwen3-30b": cls.QWEN3_30B,
            "qwen3-next-80b": cls.QWEN3_NEXT_80B,
            "qwen3-coder-480b": cls.QWEN3_CODER_480B,

            # Llama
            "llama-2-70b": cls.LLAMA_3_3_70B,
            "llama-2-13b": cls.LLAMA_4_MAVERICK,

            # Google
            "gemini-pro": cls.GEMINI_2_5_FLASH,
            "palm-2": cls.GEMINI_2_5_PRO,

            # Mistral
            "mistral-7b": cls.MISTRAL_7B,
            "mixtral-8x7b": cls.MIXTRAL_8X7B,

            # Perplexity
            "perplexity-sonar-deep-research": cls.PERPLEXITY_SONAR_DEEP_SEARCH,
            "perplexity-sonar": cls.PERPLEXITY_SONAR,

        }

    @classmethod
    def get_model_by_provider(cls, provider: str) -> List[str]:
        """제공자별 모델 목록"""
        all_models = cls.get_all_models()
        return [model_id for model_id in all_models.values() if provider.lower() in model_id.lower()]
