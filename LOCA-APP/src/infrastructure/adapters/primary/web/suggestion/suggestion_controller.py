import logging
from fastapi import APIRouter, HTTPException, status, Request, Response
from typing import List

from configuration.settings.logger.logger_config import get_logger
from .schemas.request_schema import SuggestionRequest
from .schemas.response_schema import SuggestionResponse
from ..common.decorators import handle_exceptions, log_request_response, validate_request, handle_gateway_integration
from ..common.response_builders import ResponseBuilder

logger = get_logger()

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
@handle_gateway_integration
async def generate_suggestions(
        request_body: SuggestionRequest,
        request: Request,
        response: Response
) -> SuggestionResponse:
    try:
        logger.info(f"Generating suggestions for thread_id: {request_body.thread_id}, message_id: {request_body.message_id}")

        dummy_suggestions = _generate_dummy_suggestions()

        meta_data = ResponseBuilder.build_success_meta(
            thread_id=request_body.thread_id,
            message_id=request_body.message_id,
            custom_message="연관질문 생성 성공"
        )

        response = SuggestionResponse(
            meta=meta_data,
            data={
                "suggestions": dummy_suggestions
            }
        )

        logger.info(f"Generated {len(dummy_suggestions)} suggestions for thread_id: {request_body.thread_id}")
        return response

    except Exception as e:
        logger.error(f"Failed to generate suggestions: {e}")
        error_response = ResponseBuilder.build_internal_error(
            "연관질문 생성 중 오류가 발생했습니다.",
            request_body.thread_id
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump()
        )


def _generate_dummy_suggestions() -> List[str]:
    # 사용자 입력에 따른 더미 연관질문 생성
    base_suggestions = [
        "다른 혜택도 있나요?",
        "신청 방법을 알려주세요",
        "자세한 조건이 궁금합니다",
        "언제까지 이용할 수 있나요?"
    ]

    return base_suggestions
