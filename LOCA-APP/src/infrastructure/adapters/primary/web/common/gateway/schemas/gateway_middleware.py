from fastapi import Request, Response
from typing import Optional, Dict, Any
import json
import asyncio
import logging
from .gateway_header import GatewayHeader
from configuration.settings.app_settings import get_settings

logger = logging.getLogger(__name__)


class GatewayProcessor:
    """설정 기반 API Gateway 요청/응답 처리기"""

    @classmethod
    async def extract_gateway_header(cls, request: Request) -> GatewayHeader:
        """요청에서 Gateway 헤더 정보 추출 (설정 기반)"""
        settings = get_settings()

        # Gateway 기능이 비활성화된 경우 기본값 반환
        if not settings.gateway.enabled:
            return cls._create_default_header()

        gateway_data = {}

        try:
            # 타임아웃 설정
            async with asyncio.timeout(settings.gateway.extraction_timeout):
                # 1. 헤더에서 추출 (활성화된 경우)
                if settings.gateway.header_mode:
                    gateway_data.update(cls._extract_from_headers(request))
                    logger.debug(f"Extracted headers: {gateway_data}")

                # 2. 바디에서 추출 (활성화되고 헤더 정보가 불충분한 경우)
                if (settings.gateway.body_mode and
                        not cls._has_required_fields(gateway_data, settings)):
                    body_data = await cls._extract_from_body(request, settings)
                    if body_data:
                        gateway_data.update({k: v for k, v in body_data.items()
                                             if k not in gateway_data or not gateway_data[k]})

        except asyncio.TimeoutError:
            logger.warning(f"Gateway info extraction timeout after {settings.gateway.extraction_timeout}s")
        except Exception as e:
            logger.error(f"Failed to extract gateway info: {e}")

        # ✅ 3. 최종 필수 필드 검증 (더 강력하게)
        logger.debug(f"Final gateway_data before validation: {gateway_data}")

        if not cls._validate_required_fields(gateway_data, settings):
            missing_fields = []
            required_fields = ["GUID", "SRC_SYS_CD", "STC_BIZ_CDD", "GRAM_PRG_NO", "GRAN_NO", "TSMT"]

            for field in required_fields:
                value = gateway_data.get(field, "")
                if not value or not str(value).strip():
                    missing_fields.append(field)

            error_msg = f"Required Gateway headers are missing or empty: {', '.join(missing_fields)}"
            logger.error(error_msg)
            logger.error(f"Received gateway data: {gateway_data}")
            raise ValueError(error_msg)

        # 4. 검증 통과 후 GatewayHeader 생성
        return cls._create_gateway_header(gateway_data, settings)

    @staticmethod
    def _extract_from_headers(request: Request) -> Dict[str, str]:
        """HTTP 헤더에서 Gateway 정보 추출"""
        extracted = {
            key: request.headers.get(key, "")
            for key in ["GUID", "SRC_SYS_CD", "STC_BIZ_CDD", "GRAM_PRG_NO", "GRAN_NO", "TSMT"]
        }
        logger.debug(f"Header extraction result: {extracted}")
        return extracted

    @staticmethod
    async def _extract_from_body(request: Request, settings) -> Optional[Dict[str, Any]]:
        """요청 바디에서 Gateway 정보 추출"""
        try:
            body = await request.body()
            if not body or len(body) > settings.gateway.max_body_size:
                return None

            data = json.loads(body)
            return data.get('COMM', {})
        except Exception as e:
            logger.warning(f"Failed to parse gateway info from body: {e}")
            return None

    @staticmethod
    def _has_required_fields(data: Dict[str, str], settings) -> bool:
        """필수 필드 존재 여부 확인 (기존 로직)"""
        required_fields = ["GUID", "SRC_SYS_CD", "STC_BIZ_CDD", "GRAM_PRG_NO", "GRAN_NO", "TSMT"]

        # 엄격한 검증 모드: 6개 필드 모두 필수
        if settings.gateway.strict_validation:
            result = all(bool(data.get(field, "").strip()) for field in required_fields)
            logger.debug(f"Strict validation result: {result}")
            return result

        # 기본 검증 모드: 설정에 따른 개별 필드 검사
        guid_ok = not settings.gateway.require_guid or bool(data.get("GUID", "").strip())
        tsmt_ok = not settings.gateway.require_tsmt or bool(data.get("TSMT", "").strip())

        # 나머지 필드들은 기본값이 있으므로 존재 여부만 확인
        src_sys_cd_ok = bool(data.get("SRC_SYS_CD", "").strip())
        stc_biz_cdd_ok = bool(data.get("STC_BIZ_CDD", "").strip())
        gram_prg_no_ok = bool(data.get("GRAM_PRG_NO", "").strip())
        gran_no_ok = bool(data.get("GRAN_NO", "").strip())

        result = (guid_ok and tsmt_ok and src_sys_cd_ok and
                  stc_biz_cdd_ok and gram_prg_no_ok and gran_no_ok)
        logger.debug(f"Basic validation result: {result}")
        return result

    @staticmethod
    def _validate_required_fields(data: Dict[str, str], settings) -> bool:
        """✅ 더 강력한 필수 필드 검증"""
        required_fields = ["GUID", "SRC_SYS_CD", "STC_BIZ_CDD", "GRAM_PRG_NO", "GRAN_NO", "TSMT"]

        # 엄격한 검증 또는 기본 검증 모두 6개 필드 필수로 변경
        for field in required_fields:
            value = data.get(field, "")
            if not value or not str(value).strip():
                logger.error(f"Missing required field: {field}, value: '{value}'")
                return False

        logger.debug("All required fields present")
        return True

    @classmethod
    def _create_gateway_header(cls, data: Dict[str, str], settings) -> GatewayHeader:
        """데이터와 설정으로부터 GatewayHeader 생성"""
        gateway_data = {
            "guid": data.get("GUID") or data.get("guid", ""),
            "src_sys_cd": data.get("SRC_SYS_CD") or data.get("src_sys_cd") or settings.gateway.default_src_sys_cd,
            "stc_biz_cdd": data.get("STC_BIZ_CDD") or data.get("stc_biz_cdd") or settings.gateway.default_stc_biz_cdd,
            "gram_prg_no": data.get("GRAM_PRG_NO") or data.get("gram_prg_no") or settings.gateway.default_gram_prg_no,
            "gran_no": data.get("GRAN_NO") or data.get("gran_no") or settings.gateway.default_gran_no,
            "tsmt": data.get("TSMT") or data.get("tsmt", "")
        }

        # 로깅
        if settings.gateway.log_gateway_info:
            logger.info(f"Gateway info created: GUID={gateway_data['guid'][:8] if gateway_data['guid'] else 'EMPTY'}...")

        if settings.gateway.log_missing_headers:
            missing = [k for k, v in gateway_data.items() if not v or not str(v).strip()]
            if missing:
                logger.debug(f"Empty gateway fields: {missing}")

        return GatewayHeader(**gateway_data)

    @classmethod
    def _create_default_header(cls) -> GatewayHeader:
        """기본 Gateway 헤더 생성"""
        settings = get_settings()
        return GatewayHeader(
            guid="",
            src_sys_cd=settings.gateway.default_src_sys_cd,
            stc_biz_cdd=settings.gateway.default_stc_biz_cdd,
            gram_prg_no=settings.gateway.default_gram_prg_no,
            gran_no=settings.gateway.default_gran_no,
            tsmt=""
        )

    @classmethod
    def set_response_headers(cls, response: Response, header: GatewayHeader):
        """응답 헤더에 Gateway 정보 설정"""
        settings = get_settings()

        if not settings.gateway.enabled:
            return

        header_dict = header.to_header_dict()
        for key, value in header_dict.items():
            if value:
                response.headers[key] = str(value)