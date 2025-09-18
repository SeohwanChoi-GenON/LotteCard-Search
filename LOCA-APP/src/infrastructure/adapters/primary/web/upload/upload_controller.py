from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from datetime import datetime
import json
import uuid
from typing import Optional, Dict, Any

from configuration.factories.logger_factory import get_logger
from infrastructure.adapters.primary.web.common.decorators import handle_exceptions, log_request_response, \
    validate_request
from infrastructure.adapters.primary.web.common.schemas.base_schemas import ErrorResponse
from infrastructure.adapters.primary.web.upload.schemas.request_schema import UploadRequest, UploadOperation
from infrastructure.adapters.primary.web.upload.schemas.response_schema import UploadResponse, UploadData, \
    UploadResponseMeta

logger = get_logger()

# 라우터 생성 (자동 발견을 위함)
upload_router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        422: {"model": ErrorResponse, "description": "유효성 검증 실패"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)


@upload_router.post("/uploads",
                    response_model=UploadResponse,
                    summary="LOCA앱 Elasticsearch 문서 업로드",
                    description="Elasticsearch 인덱스에 문서를 적재/수정/삭제합니다.")
@handle_exceptions
@log_request_response
@validate_request
async def upload_document(
        file: Optional[UploadFile] = File(None, description="적재 파일"),
        request: UploadRequest = Form(...)
) -> UploadResponse:
    try:
        logger.info(f"Processing upload request for index: {request.index_name}, operator: {request.operator}")

        # 메타데이터 JSON 파싱 검증
        try:
            parsed_metadata = json.loads(request.metadata)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in metadata: {e}")

        # 연산별 유효성 검증
        if request.operator in [UploadOperation.INSERT, UploadOperation.UPDATE] and not file:
            raise ValueError("Insert 및 Update 연산에는 파일이 필요합니다.")

        # 파일 정보 추출
        file_info = None
        if file:
            # 파일 크기 체크 (예: 100MB 제한)
            if hasattr(file, 'size') and file.size and file.size > 100 * 1024 * 1024:
                raise ValueError("파일 크기는 100MB를 초과할 수 없습니다.")

            file_info = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": getattr(file, 'size', 0)
            }

        # 현재는 더미 구현 - 추후 Use Case로 대체될 예정
        response_data = await _process_upload_dummy(
            file=file,
            request=request,
            metadata=parsed_metadata,
            file_info=file_info
        )

        logger.info(f"Upload processing completed for index: {request.index_name}, document_id: {response_data.data.document_id}")
        return response_data

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "VALIDATION_ERROR",
                "error_message": str(e),
                "details": {"index_name": request.index_name, "operator": request.operator.value}
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error processing upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_ERROR",
                "error_message": "파일 업로드 중 오류가 발생했습니다.",
                "details": {"index_name": request.index_name}
            }
        )


async def _process_upload_dummy(
        file: Optional[UploadFile],
        request: UploadRequest,
        metadata: dict,
        file_info: Optional[Dict[str, Any]]
) -> UploadResponse:
    """더미 업로드 처리 로직"""

    # 업로드 ID 생성
    upload_id = f"upload_{str(uuid.uuid4())[:8]}"

    # 연산별 문서 ID 생성
    if request.operator == UploadOperation.DELETE:
        # DELETE의 경우 메타데이터에서 document_id를 가져올 수 있음
        document_id = metadata.get('document_id', f"deleted_{request.index_name}_{str(uuid.uuid4())[:8]}")
    else:
        document_id = f"{request.operator.value.lower()}_{request.index_name}_{str(uuid.uuid4())[:8]}"

    # 파일 처리 시뮬레이션 (실제로는 Elasticsearch 처리)
    if file:
        logger.info(f"Processing file: {file.filename}")
        # 실제 구현시에는 여기서 파일 내용을 읽어서 Elasticsearch에 인덱싱
        # content = await file.read()
        # elasticsearch_service.index_document(request.index_name, document_id, content, metadata)

    # 메타데이터 로깅
    logger.info(f"Metadata: {metadata}")

    # 응답 구성
    response = UploadResponse(
        meta=UploadResponseMeta(
            upload_id=upload_id,
            result_status="200",
            result_status_message=f"{request.operator.value} 작업이 성공적으로 완료되었습니다.",
            timestamp=datetime.now()
        ),
        data=UploadData(
            document_id=document_id,
            created_at=datetime.now(),
            index_name=request.index_name,
            operation=request.operator.value,
            file_info=file_info
        )
    )

    return response