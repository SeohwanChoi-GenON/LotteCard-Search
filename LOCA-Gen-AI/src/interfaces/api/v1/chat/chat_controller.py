from datetime import datetime
from fastapi import APIRouter

from interfaces.api.schemas.chat.chat_schema import ChatResponse, ChatRequest
from interfaces.api.schemas.chat.meta.meta_schema import ChatMetaResponse
from interfaces.api.schemas.chat.data.data_schema import ChatDataResponse
from interfaces.api.schemas.chat.context.context_schema import ChatContextResponse, RetrievedContext, DocumentMetadata

chat_router = APIRouter(prefix='/chat', tags=['chat'])


@chat_router.post(
    path="/",
    response_model=ChatResponse,
    summary="LOCA 통합 챗봇",
    description="사용자 질문에 대한 AI 챗봇 응답을 생성합니다."
)
async def chat_controller(
        request: ChatRequest
) -> ChatResponse:
    print(f"User Input: {request.user_input}")
    print(f"Thread ID: {request.thread_id}")

    # 더미 메타 데이터
    meta = ChatMetaResponse(
        result_status="SUCCESS",
        result_status_message="정상 처리되었습니다.",
        timestamp=datetime.now(),
        thread_id=request.thread_id,
        message_id=1
    )

    # 더미 데이터 응답
    data = ChatDataResponse(
        general_answer=f"안녕하세요! '{request.user_input}'에 대한 답변을 준비하고 있습니다. 곧 더 자세한 정보를 제공해드릴게요.",
        general_answer_template=None
    )

    # 더미 컨텍스트 데이터 - DocumentMetadata 구조에 맞게 수정
    context = ChatContextResponse(
        retrieved_contexts=[
            RetrievedContext(
                metadata=DocumentMetadata(
                    chunk_id="chunk_001",
                    section_name="FAQ 섹션",
                    page_number=1,
                    source="FAQ 데이터베이스"
                ),
                page_content="자주 묻는 질문에 대한 답변 내용입니다."
            ),
            RetrievedContext(
                metadata=DocumentMetadata(
                    chunk_id="chunk_002",
                    section_name="상품 정보 섹션",
                    page_number=2,
                    source="상품 정보 데이터베이스"
                ),
                page_content="롯데카드 상품 관련 정보 내용입니다."
            )
        ]
    )

    return ChatResponse(
        meta=meta,
        data=data,
        context=context
    )