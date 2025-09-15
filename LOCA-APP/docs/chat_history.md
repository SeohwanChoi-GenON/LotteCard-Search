# LOCA 챗봇 API 인터페이스 문서

## 1. AIG-LOCA-001: 대화이력저장 - 첫턴

**엔드포인트**: `/GAI/GC/CHSLG0001I` | **HTTP Method**: `POST`  
**데이터 송신**: FastAPI WebApp → **데이터 수신**: Oracle

### Request Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 예시 |
|---------|--------|-----------|------|------|------|------|
| COMM | GUID | string | 31 | Y | Global Unique ID (31자리)<br/>yyyyMMdd(8) + 기관영문(n) + 전문생성일시(hhmmSSsss(9) + 일련번호(n) | 20250819ABCD135911234AAAAABBBBB |
| COMM | SRC_SYS_CD | string | 3 | Y | 요청 출발지 시스템 코드 3자리 | GAI |
| COMM | STC_BIZ_CDD | string | 2 | Y | 요청 출발지 업무 코드 2자리 | AT |
| COMM | GRAM_PRG_NO | string | - | Y | 전문 진행번호(=00) | 0 |
| COMM | GRAN_NO | string | - | Y | 전문 번호(=N) | N |
| COMM | TSMT | string | - | Y | 요청 타임스탬프 (yyyyMMddhhmmssSSS) | - |
| DATA | USER_ID | string | - | Y | 사용자 사번 | PJ04481 |
| DATA | SERVICE_ID | string | - | Y | 서비스ID | 01 |
| DATA | UUID | string | - | Y | 쓰레드(UUID) | - |
| DATA | **MESSAGES** | **list** | - | **Y** | **메시지 리스트** | - |
| DATA | └ role | string | - | Y | 메시지 역할 | user, assistant, file |
| DATA | └ content | string | - | Y | 메시지 내용 | "안녕하세요" |
| DATA | └ additional_kwargs | dict | - | N | 추가 메타데이터 | {"created_date": "...", "msg_id": "..."} |
| DATA | └ created_date | string | - | Y | 생성일시(ISO표준) | 2025-09-01T01:00:00:001+09:00 |
| DATA | └ msg_no | int | - | Y | 메시지 번호 | 25, 26, 27 |
| DATA | THREAD_TITLE | string | - | N | 대화 제목 | - |

### Response Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 제약조건 |
|---------|--------|-----------|------|------|------|---------|
| COMM | GUID | - | - | - | - | - |
| COMM | SRC_SYS_CD | - | - | - | - | - |
| COMM | STC_BIZ_CDD | - | - | - | - | - |
| COMM | GRAM_PRG_NO | - | - | - | - | - |
| COMM | GRAN_NO | - | - | - | - | - |
| COMM | TSMT | - | - | - | - | - |
| DATA | RESULT | string | - | Y | 처리결과 | "SUCCESS" |

### 수행로직
첫 턴은 첫번째 질의와 응답을 기록하고, 필요 시 대화제목을 저장할 수 있도록 함. 각 대화목록의 생성 시각은 첫 턴의 user 질의 created_date값으로 함. **대화 이력 DB 기록**. 동일 스레드에 대해 첫 턴 API를 2회 이상 호출하는 경우 오류.

---

## 2. AIG-LOCA-002: 대화이력저장 - 후속턴

**엔드포인트**: `/GAI/GC/CHSLG0002I` | **HTTP Method**: `POST`  
**데이터 송신**: FastAPI WebApp → **데이터 수신**: Oracle

### Request Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 예시 |
|---------|--------|-----------|------|------|------|------|
| COMM | GUID | string | 31 | Y | Global Unique ID (31자리) | 20250819ABCD135911234AAAAABBBBB |
| COMM | SRC_SYS_CD | string | 3 | Y | 요청 출발지 시스템 코드 3자리 | GAI |
| COMM | STC_BIZ_CDD | string | 2 | Y | 요청 출발지 업무 코드 2자리 | AT |
| COMM | GRAM_PRG_NO | string | - | Y | 전문 진행번호(=00) | 0 |
| COMM | GRAN_NO | string | - | Y | 전문 번호(=N) | N |
| COMM | TSMT | string | - | Y | 요청 타임스탬프 (yyyyMMddhhmmssSSS) | - |
| DATA | USER_ID | string | - | Y | 사용자 사번 | PJ04481 |
| DATA | SERVICE_ID | string | - | Y | 서비스ID | 01 |
| DATA | UUID | string | - | Y | 쓰레드(UUID) | - |
| DATA | **MESSAGES** | **list** | - | **Y** | **메시지 리스트** | - |
| DATA | └ role | string | - | Y | 메시지 역할 | user, assistant, file |
| DATA | └ content | string | - | Y | 메시지 내용 | "안녕하세요" |
| DATA | └ additional_kwargs | dict | - | N | 추가 메타데이터 | {"created_date": "...", "msg_id": "..."} |
| DATA | └ created_date | string | - | Y | 생성일시(ISO표준) | 2025-09-01T01:00:00:001+09:00 |
| DATA | └ msg_no | int | - | Y | 메시지 번호 | 25, 26, 27 |

### Response Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 제약조건 |
|---------|--------|-----------|------|------|------|---------|
| COMM | GUID | - | - | - | - | - |
| COMM | SRC_SYS_CD | - | - | - | - | - |
| COMM | STC_BIZ_CDD | - | - | - | - | - |
| COMM | GRAM_PRG_NO | - | - | - | - | - |
| COMM | GRAN_NO | - | - | - | - | - |
| COMM | TSMT | - | - | - | - | - |
| DATA | RESULT | string | - | Y | 처리결과 | "SUCCESS" |

### 수행로직
**대화여력저장 - 후속 턴**은 대화 이력만 저장. 첫 턴 기록이 없을 경우 오류 처리 함.

---

## 3. AIG-LOCA-003: 대화제목설정/변경

**엔드포인트**: `/GAI/GC/CHSNM0001I` | **HTTP Method**: `POST`  
**데이터 송신**: FastAPI WebApp → **데이터 수신**: Oracle

### Request Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 예시 |
|---------|--------|-----------|------|------|------|------|
| COMM | GUID | string | 31 | Y | Global Unique ID (31자리) | 20250819ABCD135911234AAAAABBBBB |
| COMM | SRC_SYS_CD | string | 3 | Y | 요청 출발지 시스템 코드 3자리 | GAI |
| COMM | STC_BIZ_CDD | string | 2 | Y | 요청 출발지 업무 코드 2자리 | AT |
| COMM | GRAM_PRG_NO | string | - | Y | 전문 진행번호(=00) | 0 |
| COMM | GRAN_NO | string | - | Y | 전문 번호(=N) | N |
| COMM | TSMT | string | - | Y | 요청 타임스탬프 (yyyyMMddhhmmssSSS) | - |
| DATA | USER_ID | string | - | Y | 사용자 사번 | PJ04481 |
| DATA | SERVICE_ID | string | - | Y | 서비스ID | 01 |
| DATA | UUID | string | - | Y | 쓰레드(UUID) | - |
| DATA | THREAD_TITLE | string | - | Y | 대화 제목 | - |

### Response Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 제약조건 |
|---------|--------|-----------|------|------|------|---------|
| COMM | GUID | - | - | - | - | - |
| COMM | SRC_SYS_CD | - | - | - | - | - |
| COMM | STC_BIZ_CDD | - | - | - | - | - |
| COMM | GRAM_PRG_NO | - | - | - | - | - |
| COMM | GRAN_NO | - | - | - | - | - |
| COMM | TSMT | - | - | - | - | - |
| DATA | RESULT | string | - | Y | 처리결과 | "SUCCESS" |

### 수행로직
대화 제목을 사용자가 직접 설정하는 등, **첫 턴 이후 제목 설정/변경**이 필요한 경우 사용. 사용자가 설정한 제목과 AI가 생성한 제목을 구분. 대화가 존재하지 않는 경우 오류 처리.

---

## 4. AIG-LOCA-004: 대화이력삭제

**엔드포인트**: `/GAI/GC/CHSLG0003D` | **HTTP Method**: `POST`  
**데이터 송신**: FastAPI WebApp → **데이터 수신**: Oracle

### Request Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 예시 |
|---------|--------|-----------|------|------|------|------|
| COMM | GUID | string | 31 | Y | Global Unique ID (31자리) | 20250819ABCD135911234AAAAABBBBB |
| COMM | SRC_SYS_CD | string | 3 | Y | 요청 출발지 시스템 코드 3자리 | GAI |
| COMM | STC_BIZ_CDD | string | 2 | Y | 요청 출발지 업무 코드 2자리 | AT |
| COMM | GRAM_PRG_NO | string | - | Y | 전문 진행번호(=00) | 0 |
| COMM | GRAN_NO | string | - | Y | 전문 번호(=N) | N |
| COMM | TSMT | string | - | Y | 요청 타임스탬프 (yyyyMMddhhmmssSSS) | - |
| DATA | USER_ID | string | - | Y | 사용자 사번 | PJ04481 |
| DATA | SERVICE_ID | string | - | Y | 서비스ID | 01 |
| DATA | UUID | string | - | Y | 쓰레드(UUID) | - |

### Response Parameters

| 시스템명 | 속성명 | 데이터타입 | 길이 | 필수 | 설명 | 제약조건 |
|---------|--------|-----------|------|------|------|---------|
| COMM | GUID | - | - | - | - | - |
| COMM | SRC_SYS_CD | - | - | - | - | - |
| COMM | STC_BIZ_CDD | - | - | - | - | - |
| COMM | GRAM_PRG_NO | - | - | - | - | - |
| COMM | GRAN_NO | - | - | - | - | - |
| COMM | TSMT | - | - | - | - | - |
| DATA | RESULT | string | - | Y | 처리결과 | "SUCCESS" |

### 수행로직
**대화 이력 삭제**. 대화 이력이 없는 경우 삭제 처리.

---

## 📝 MESSAGES 구조 상세 예시

```json
CHAT_CONTENTS = [
  {
    "role": "file", 
    "content": "???", 
    "additional_kwargs": {...}, 
    "created_date": "2025-09-05 12:23:00", 
    "msg_no": 25
  }, 
  {
    "role": "user", 
    "content": "???", 
    "additional_kwargs": {...}, 
    "created_date": "2025-09-05 12:23:00", 
    "msg_no": 26
  }, 
  {
    "role": "assistant", 
    "content": "???", 
    "additional_kwargs": {...}, 
    "created_date": "2025-09-05 12:23:00", 
    "msg_no": 27
  }
]
```