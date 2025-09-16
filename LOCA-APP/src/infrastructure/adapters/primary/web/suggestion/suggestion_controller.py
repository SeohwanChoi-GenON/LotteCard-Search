import logging
from fastapi import APIRouter, HTTPException, status
from typing import List

from .schemas.request_schema import SuggestionRequest
from .schemas.response_schema import SuggestionResponse
from ..common.decorators import handle_exceptions, log_request_response, validate_request
from ..common.response_builders import ResponseBuilder

logger = logging.getLogger(__name__)

suggestion_router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@suggestion_router.post(
    "/suggestions",
    response_model=SuggestionResponse,
    summary="연관질문 생성",
    description="사용자의 질문과 대화 컨텍스트를 바탕으로 연관질문을 생성합니다."
)
@handle_exceptions
@log_request_response
@validate_request
async def generate_suggestions(request: SuggestionRequest) -> SuggestionResponse:
    try:
        logger.info(f"Generating suggestions for thread_id: {request.thread_id}, message_id: {request.message_id}")

        dummy_suggestions = _generate_dummy_suggestions(request.user_input)

        meta_data = ResponseBuilder.build_success_meta(
            thread_id=request.thread_id,
            message_id=request.message_id,
            custom_message="연관질문 생성 성공"
        )

        response = SuggestionResponse(
            meta=meta_data,
            data={
                "suggestions": dummy_suggestions
            }
        )

        logger.info(f"Generated {len(dummy_suggestions)} suggestions for thread_id: {request.thread_id}")
        return response

    except Exception as e:
        logger.error(f"Failed to generate suggestions: {e}")
        error_response = ResponseBuilder.build_internal_error(
            "연관질문 생성 중 오류가 발생했습니다.",
            request.thread_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )


def _generate_dummy_suggestions(user_input: str) -> List[str]:
    # 사용자 입력에 따른 더미 연관질문 생성
    base_suggestions = [
        "다른 혜택도 있나요?",
        "신청 방법을 알려주세요",
        "자세한 조건이 궁금합니다",
        "언제까지 이용할 수 있나요?",
        "비슷한 다른 서비스는 어떤게 있나요?"
    ]

    if "카드" in user_input:
        return [
            "다른 카드 혜택도 있나요?",
            "카드 신청 방법을 알려주세요",
            "연회비는 얼마인가요?",
            "카드 사용 조건이 궁금합니다"
        ]
    elif "할인" in user_input:
        return [
            "할인율은 얼마나 되나요?",
            "할인 받는 방법을 알려주세요",
            "다른 할인 혜택도 있나요?",
            "할인 기간은 언제까지인가요?"
        ]
    elif "이벤트" in user_input:
        return [
            "이벤트 참여 방법을 알려주세요",
            "이벤트 기간은 언제까지인가요?",
            "다른 진행중인 이벤트는?",
            "이벤트 혜택을 자세히 알려주세요"
        ]
    else:
        return base_suggestions[:4]  # 기본 4개 반환
