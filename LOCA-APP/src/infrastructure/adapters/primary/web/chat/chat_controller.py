"""
Chat 컨트롤러

채팅 관련 API 엔드포인트를 처리합니다.
"""

from fastapi import APIRouter
from datetime import datetime
import logging
from typing import Dict

from .schemas import (
    ChatRequest,
    ChatResponse,
    ChatResponseMeta,
    ChatResponseData,
    ChatResponseContext
)
from ..common.base_schemas import ErrorResponse, RetrievedContent
from ..common.decorators import handle_exceptions, log_request_response, validate_request
from ..common.response_builders import ResponseBuilder

logger = logging.getLogger(__name__)

# 라우터 생성 (자동 발견을 위함)
chat_router = APIRouter(
    prefix="/loca-talk",
    tags=["loca-talk"],
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)

# 메시지 ID 카운터 (실제로는 데이터베이스나 캐시에서 관리)
message_counters: Dict[str, int] = {}


def get_next_message_id(thread_id: str) -> int:
    """스레드별 다음 메시지 ID 생성"""
    if thread_id not in message_counters:
        message_counters[thread_id] = 0
    message_counters[thread_id] += 1
    return message_counters[thread_id]


@chat_router.post(
    "/chat",
    response_model=ChatResponse,
    summary="LOCA앱 통합 챗봇",
    description="사용자 질문을 받아 AI가 생성한 답변을 반환합니다."
)
@handle_exceptions
@log_request_response
@validate_request
async def process_chat(request: ChatRequest) -> ChatResponse:
    """
    LOCA앱 통합 챗봇 엔드포인트

    - **thread_id**: 대화 세션 고유 ID
    - **user_id**: 사용자 ID
    - **service_id**: 서비스 식별자 (Unified, Card, Event, Contents, Commerce, Menu)
    - **user_input**: 사용자 질문 내용
    """
    # 현재는 더미 구현 - 추후 Use Case로 대체될 예정
    return await _process_chat_dummy(request)


async def _process_chat_dummy(request: ChatRequest) -> ChatResponse:
    """
    더미 채팅 처리 로직
    추후 실제 Use Case로 대체될 예정
    """

    # 간단한 키워드 기반 응답 생성
    answer = _generate_dummy_answer(request.user_input, request.service_id.value)

    # 더미 검색 결과
    retrieved_contents = ResponseBuilder.build_dummy_retrieved_contents(request.user_input)

    # 메시지 ID 생성
    message_id = get_next_message_id(request.thread_id)

    # 응답 구성
    response = ChatResponse(
        meta=ChatResponseMeta(
            thread_id=request.thread_id,
            message_id=message_id,
            result_status="200",
            result_status_message="성공",
            timestamp=datetime.now()
        ),
        data=ChatResponseData(
            general_answer=answer,
            general_answer_template=None  # 현재는 템플릿 미사용
        ),
        context=ChatResponseContext(
            retrieved_contents=retrieved_contents
        )
    )

    return response


def _generate_dummy_answer(user_input: str, service_id: str) -> str:
    """더미 답변 생성"""

    keywords_responses = {
        "할인": f"현재 {service_id} 서비스에서 다양한 할인 혜택을 제공하고 있습니다. 롯데카드를 이용하시면 추가 할인 혜택을 받으실 수 있습니다.",
        "카드": "롯데카드의 다양한 카드 상품을 확인해보세요. SUPER RED, PINK 등 다양한 옵션이 있습니다.",
        "이벤트": "현재 진행 중인 이벤트를 확인해보시기 바랍니다. 다양한 혜택과 경품이 준비되어 있습니다.",
        "포인트": "롯데포인트를 적립하고 사용하는 방법에 대해 안내해드리겠습니다.",
        "문의": "더 자세한 문의사항이 있으시면 고객센터로 연락주시기 바랍니다."
    }

    user_input_lower = user_input.lower()

    for keyword, response in keywords_responses.items():
        if keyword in user_input_lower:
            return f"{response}\n\n문의하신 '{user_input}'에 대한 더 자세한 정보가 필요하시면 언제든 말씀해 주세요."

    return f"'{user_input}'에 대한 질문을 주셔서 감사합니다. 관련 정보를 찾아서 도움을 드리겠습니다. 더 구체적인 질문이 있으시면 언제든 말씀해 주세요."


@chat_router.get(
    "/health",
    summary="채팅 서비스 상태 확인",
    description="채팅 서비스의 상태를 확인합니다."
)
async def health_check():
    """채팅 서비스 헬스체크"""
    return {
        "status": "healthy",
        "service": "chat_controller",
        "timestamp": datetime.now()
    }