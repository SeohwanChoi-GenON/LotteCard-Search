import asyncio

from client.openrouter.multi_model_manager import MultiModelManager
from settings import get_settings

class OpenRouterConfig:
    """OpenRouter 설정을 하나의 클래스로 관리"""

    def __init__(self):
        # **모델 선택** (사용하고 싶은 모델들)
        self.selected_models = [
            "claude-4-sonnet",
            "gpt-4.1-mini",
            "qwen3-next-80b",
            "gpt-oss"
        ]

        # **메시지 설정**
        self.user_message = "Supervisor Agent에 대해서 핵심 내용만 알려주세요."

        # **요청 설정**
        self.temperature = 0.2
        self.max_tokens = 200
        self.stream_mode = False  # True: 스트림, False: 일반

        # **테스트 모드 선택**
        self.test_mode = "single"  # "single", "compare", "stream", "provider"


async def run_single_model(config: OpenRouterConfig):
    """단일 모델 실행"""
    print("=== **단일 모델 테스트** ===")

    settings = get_settings()
    manager = MultiModelManager(settings)

    # 첫 번째 모델 사용
    selected_model = config.selected_models[0]
    messages = [{"role": "user", "content": config.user_message}]

    print(f"**사용 모델**: {selected_model}")
    print(f"**질문**: {config.user_message}")
    print("-" * 50)

    if config.stream_mode:
        print("**스트림 응답**:")
        stream_response = await manager.chat_with_model(
            model_name=selected_model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            stream=True
        )

        content = ""
        async for chunk in stream_response:
            if "choices" in chunk and chunk["choices"]:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    chunk_content = delta["content"]
                    print(chunk_content, end="", flush=True)
                    content += chunk_content

                finish_reason = chunk["choices"][0].get("finish_reason")
                if finish_reason:
                    print(f"\n\n**완료**: {finish_reason}")
                    break
    else:
        response = await manager.chat_with_model(
            model_name=selected_model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            stream=False
        )

        content = response["choices"][0]["message"]["content"]
        usage = response.get("usage", {})

        print(f"**응답**: {content}")
        print(f"**토큰 사용량**: {usage}")


async def run_model_comparison(config: OpenRouterConfig):
    """모델 비교 실행"""
    print("=== **모델 비교 테스트** ===")

    settings = get_settings()
    manager = MultiModelManager(settings)

    messages = [{"role": "user", "content": config.user_message}]

    print(f"**비교 모델들**: {config.selected_models}")
    print(f"**질문**: {config.user_message}")
    print("-" * 50)

    results = await manager.compare_models(
        model_names=config.selected_models,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )

    for i, (model_name, result) in enumerate(results.items(), 1):
        print(f"\n**{i}. {model_name}**")
        if "error" in result:
            print(f"❌ 오류: {result['error']}")
        else:
            print(f"✅ 응답: {result['response']}")
            print(f"📊 토큰: {result.get('usage', {})}")
        print("-" * 30)


async def run_stream_multiple(config: OpenRouterConfig):
    """다중 모델 스트림 실행"""
    print("=== **다중 모델 스트림 테스트** ===")

    settings = get_settings()
    manager = MultiModelManager(settings)

    messages = [{"role": "user", "content": config.user_message}]

    print(f"**스트림 모델들**: {config.selected_models}")
    print(f"**질문**: {config.user_message}")
    print("-" * 50)

    await manager.stream_multiple_models(
        model_names=config.selected_models,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )


async def run_provider_analysis(config: OpenRouterConfig):
    """제공자별 분석 실행"""
    print("=== **제공자별 모델 분석** ===")

    settings = get_settings()
    manager = MultiModelManager(settings)

    providers = ["openai", "anthropic", "qwen", "google"]

    for provider in providers:
        models = manager.models.get_model_by_provider(provider)
        print(f"**{provider.upper()} 모델들**:")
        for model in models:
            print(f"  - {model}")
        print()


async def main():
    """메인 실행 함수 - 설정을 하나의 변수로 관리"""

    # ========================================
    # 🎯 **여기서 모든 설정을 관리하세요!**
    # ========================================

    config = OpenRouterConfig()

    # **원하는 설정으로 변경**
    config.selected_models = [
        "claude-4-sonnet",
        "gpt-4.1-mini",
        "qwen3-next-80b",
        "gpt-oss"
    ]

    config.user_message = "Supervisor Agent에 대해서 핵심 내용만 알려주세요."

    config.temperature = 0.2  # 창의성 (0.0 ~ 1.0)
    config.max_tokens = 200  # 최대 토큰 수
    config.stream_mode = False  # True: 실시간 스트림, False: 일반 응답
    config.test_mode = "single"  # "single", "compare", "stream", "provider"

    # ========================================
    # 🚀 **선택된 모드 실행**
    # ========================================

    print(f"🔧 **설정 정보**")
    print(f"모델: {config.selected_models}")
    print(f"질문: {config.user_message}")
    print(f"온도: {config.temperature}, 토큰: {config.max_tokens}")
    print(f"스트림: {config.stream_mode}, 모드: {config.test_mode}")
    print("=" * 60)

    # 모드별 실행
    if config.test_mode == "single":
        await run_single_model(config)

    elif config.test_mode == "compare":
        await run_model_comparison(config)

    elif config.test_mode == "stream":
        config.stream_mode = True  # 스트림 모드 강제 활성화
        await run_stream_multiple(config)

    elif config.test_mode == "provider":
        await run_provider_analysis(config)

    else:
        print("❌ 지원하지 않는 테스트 모드입니다.")
        print("사용 가능한 모드: single, compare, stream, provider")


if __name__ == "__main__":
    asyncio.run(main())