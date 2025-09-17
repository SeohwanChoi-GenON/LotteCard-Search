"""API Gateway 헤더 처리를 위한 기술적 Value Object"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class GatewayHeader(BaseModel):
    """API Gateway 헤더 정보 - 기술적 VO

    주의: 이는 비즈니스 도메인 객체가 아닌 인프라스트럭처 기술 객체입니다.
    Gateway와의 통신을 위한 기술적 요구사항을 캡슐화합니다.
    """

    guid: str = Field(..., description="Global Unique ID")
    src_sys_cd: str = Field("GAI", description="출발지 시스템 코드")
    stc_biz_cdd: str = Field("BR", description="출발지 업무 코드")
    gram_prg_no: str = Field("00", description="전문 진행번호")
    gran_no: str = Field("N", description="전문 번호")
    tsmt: str = Field(..., description="요청 타임스탬프")

    class Config:
        """Pydantic 설정"""
        frozen = True  # 불변 객체로 만들기
        allow_mutation = False

    def __str__(self) -> str:
        """문자열 표현"""
        return f"GatewayHeader(GUID={self.guid}, SRC={self.src_sys_cd}, TSMT={self.tsmt})"

    def to_header_dict(self) -> Dict[str, str]:
        """HTTP 헤더용 딕셔너리 변환"""
        return {
            "GUID": self.guid,
            "SRC_SYS_CD": self.src_sys_cd,
            "STC_BIZ_CDD": self.stc_biz_cdd,
            "GRAM_PRG_NO": self.gram_prg_no,
            "GRAN_NO": self.gran_no,
            "TSMT": self.tsmt
        }

    def to_dict(self) -> Dict[str, str]:
        """일반 딕셔너리 변환"""
        return self.dict()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GatewayHeader":
        """딕셔너리에서 객체 생성"""
        return cls(
            guid=data.get("GUID") or data.get("guid", ""),
            src_sys_cd=data.get("SRC_SYS_CD") or data.get("src_sys_cd", "GAI"),
            stc_biz_cdd=data.get("STC_BIZ_CDD") or data.get("stc_biz_cdd", "BR"),
            gram_prg_no=data.get("GRAM_PRG_NO") or data.get("gram_prg_no", "00"),
            gran_no=data.get("GRAN_NO") or data.get("gran_no", "N"),
            tsmt=data.get("TSMT") or data.get("tsmt", "")
        )


# 하위 호환성을 위한 별칭 (기존 HeaderInfo와 호환)
HeaderInfo = GatewayHeader