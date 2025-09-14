# API 명세서

## LOCA앱 API

### 1. LOCA앱 통합 챗봇 (AIG-LOCA-001)

| 구분 | 내용 |
|------|------|
| **엔드포인트** | `/api/v1/loca-talk/chat` |
| **HTTP Method** | POST |
| **Tags** | loca-talk |

#### Request Parameters
| 속성명 | 데이터 타입 | 길이 | 필수 | 설명 | 제약조건 |
|--------|-------------|------|------|------|----------|
| thread_id | string | 50 | Y | 대화 세션 고유 ID | |
| user_id | string | 20 | Y | 사용자 ID | |
| service_id | string | 20 | Y | 서비스 식별자 | enum: ["Unified", "Card", "Event", "Contents", "Commerce", "Menu"] |
| user_input | string | 1000 | Y | 사용자 질문 내용 | |

#### Response Parameters
| 속성명 | 데이터 타입 | 길이 | 필수 | 설명 | 제약조건 |
|--------|-------------|------|------|------|----------|
| **meta.thread_id** | string | 50 | Y | 대화 세션 고유 ID | |
| **meta.message_id** | number | - | Y | 메시지 인덱스 | |
| **meta.result_status** | string | 20 | Y | 처리 상태 | HTTP Status Code |
| **meta.result_status_message** | string | 1000 | Y | 처리 상태 메시지 | |
| **meta.timestamp** | string | 50 | Y | 타임 스탬프 | iso-datetime |
| **data.general_answer** | string | 5000 | Y | AI 생성 답변 | |
| **data.general_answer_template** | object | - | N | 템플릿 답변 구조 | 정의된 템플릿 구조 답변 |
| **context.retrieved_contents** | object | - | N | 관련 문서 목록 | object 타입 세부 스펙 추후 결정 |

---

