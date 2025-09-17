from fastapi import APIRouter, Request, Response
from datetime import datetime
import logging
from typing import Dict

from configuration.settings.logger.logger_config import get_logger
from infrastructure.adapters.primary.web.common.schemas.base_schemas import ErrorResponse
from .schemas.request_schema import CompletionRequest
from .schemas.response_schema import CompletionResponse, CompletionResponseMeta, CompletionResponseData
from infrastructure.adapters.primary.web.common.gateway.HeaderInfo import HeaderInfo
from ..common.decorators import handle_exceptions, log_request_response, validate_request, handle_gateway_integration
from ..common.gateway.schemas.gateway_middleware import GatewayProcessor

logger = get_logger()

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
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
    "/completions",
    response_model=CompletionResponse,
    summary="LOCA앱 통합 챗봇",
    description="사용자 질문을 받아 AI가 생성한 답변을 반환합니다."
)
@handle_exceptions
@log_request_response
@validate_request
@handle_gateway_integration
async def process_chat(
        request_body: CompletionRequest,
        request: Request,
        response: Response
) -> CompletionResponse:
    print(request.headers)

    return await _process_chat_dummy(request_body)

async def _process_chat_dummy(request: CompletionRequest) -> CompletionResponse:
    answer = _generate_dummy_answer(request.user_input, request.service_id.value)
    message_id = get_next_message_id(request.thread_id)

    response = CompletionResponse(
        meta=CompletionResponseMeta(
            thread_id=request.thread_id,
            message_id=message_id,
            result_status="200",
            result_status_message="성공",
            timestamp=datetime.now()
        ),
        data=CompletionResponseData(
            general_answer=answer,
            general_answer_template="TBD"
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
