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

