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

### 3. LOCA앱 연관질문 생성 (AIG-LOCA-003)

| 구분            | 내용                             |
| --------------- |--------------------------------|
| **엔드포인트**  | `/api/v1/loca-talk/suggestion` |
| **HTTP Method** | POST                           |
| **Tags**        | loca-talk                      |

#### Request Parameters

| 속성명                 | 데이터 타입 | 길이 | 필수 | 설명              | 제약조건                                                     |
|---------------------| ----------- | ---- | ---- | ----------------- | ------------------------------------------------------------ |
| thread_id           | string      | 50   | Y    | 대화 세션 고유 ID |                                                              |
| message_id          | number      | -    | Y    | 메시지 인덱스     |                                                              |
| service_id          | string      | 20   | Y    | 서비스 식별자     | enum: ["Unified", "Card", "Event", "Contents", "Commerce", "Menu"] |
| user_input          | string      | 1000 | Y    | 사용자 질문 내용  |                                                              |
| retrieved_contents  | array       | -    | -    | 검색된 문서 목록  |                                                              |
| generated_answer    | string      | 5000 | -    | LLM 답변 내용     |                                                              |

#### Response Parameters

| 속성명               | 데이터 타입 | 필수 | 설명           |
| -------------------- | ----------- | ---- | -------------- |
| **meta**             | -           | -    | 공통 메타 정보 |
| **data.suggestions** | array       | N    | 추천 연관 질문 |

---

### 6. LOCA앱 수동 업로드 API (AIG-LOCA-006)

| 구분            | 내용                          |
| --------------- |-----------------------------|
| **엔드포인트**  | `/api/v1/loca-talk/uploads` |
| **HTTP Method** | POST                        |
| **Tags**        | loca-talk                   |

#### Request Parameters

| 속성명     | 데이터 타입   | 길이 | 필수 | 설명            | 제약조건                           |
| ---------- | ------------- | ---- | ---- | --------------- | ---------------------------------- |
| file       | MultipartFile | -    | N    | 적재 파일       |                                    |
| index_name | string        | 200  | Y    | 인덱스명        |                                    |
| metadata   | string        | 1000 | Y    | 적재 메타데이터 | TBD(추후 구체화 필요)              |
| operator   | string        | 50   | Y    | CRUD 기능 선택  | enum["Insert", "Update", "Delete"] |

#### Response Parameters

| 속성명               | 데이터 타입 | 필수 | 설명                | 제약조건     |
| -------------------- | ----------- | ---- | ------------------- | ------------ |
| **data.document_id** | string      | Y    | 생성/수정된 문서 ID |              |
| **data.created_at**  | string      | Y    | 문서의 생성된 시간  | iso-datetime |

------

## 
