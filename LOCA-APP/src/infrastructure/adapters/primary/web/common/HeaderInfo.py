from pydantic import BaseModel
from fastapi import Request, Response

class HeaderInfo(BaseModel):
    guid: str
    src_sys_cd: str = "GAI"
    stc_biz_cdd: str = "BR"
    gram_prg_no: str = "00"
    gran_no: str = "N"
    tsmt: str


class HeaderProcessor:
    """헤더 처리 전용 클래스"""

    HEADER_MAPPINGS = {
        "GUID": "guid",
        "SRC_SYS_CD": "src_sys_cd",
        "STC_BIZ_CDD": "stc_biz_cdd",
        "GRAM_PRG_NO": "gram_prg_no",
        "GRAN_NO": "gran_no",
        "TSMT": "tsmt"
    }

    @classmethod
    def extract_from_request(cls, request: Request) -> HeaderInfo:
        """요청 헤더에서 정보 추출"""
        return HeaderInfo(
            guid=request.headers.get("GUID"),
            src_sys_cd=request.headers.get("SRC_SYS_CD", "GAI"),
            stc_biz_cdd=request.headers.get("STC_BIZ_CDD", "BR"),
            gram_prg_no=request.headers.get("GRAM_PRG_NO", "00"),
            gran_no=request.headers.get("GRAN_NO", "N"),
            tsmt=request.headers.get("TSMT")
        )

    @classmethod
    def set_response_headers(cls, response: Response, header_info: HeaderInfo):
        """응답 헤더 설정"""
        for header_name, field_name in cls.HEADER_MAPPINGS.items():
            value = getattr(header_info, field_name, "")
            if value:  # None이나 빈 문자열이 아닌 경우만
                response.headers[header_name] = str(value)