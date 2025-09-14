# LOCA 앱

## 구성도
```
src/
├── main.py                              # 애플리케이션 진입점
├── domain/
│   ├── model/
│   │   ├── conversation/
│   │   │   ├── thread.py                # 대화 세션 (Aggregate Root)
│   │   │   ├── message.py               # 메시지 (Entity)
│   │   │   ├── user_query.py            # 사용자 질의 (Value Object)
│   │   │   └── chat_response.py         # 챗봇 응답 (Value Object)
│   │   ├── search/
│   │   │   ├── search_intent.py         # 검색 의도 (Value Object)
│   │   │   ├── document.py              # 검색 문서 (Value Object)
│   │   │   └── search_result.py         # 검색 결과 (Value Object)
│   │   ├── suggestion/                  # 연관질문 도메인
│   │   │   ├── suggestion.py            # 연관질문 (Value Object)
│   │   │   └── suggestion_context.py    # 연관질문 컨텍스트 (Value Object)
│   │   ├── upload/                      # 업로드 도메인
│   │   │   ├── document_upload.py       # 문서 업로드 (Aggregate Root)
│   │   │   ├── upload_metadata.py       # 업로드 메타데이터 (Value Object)
│   │   │   └── upload_operation.py      # 업로드 연산 타입 (Value Object)
│   │   └── common/
│   │       ├── thread_id.py             # Thread ID (Value Object)
│   │       ├── user_id.py               # User ID (Value Object)
│   │       └── service_id.py            # Service ID (Value Object)
│   ├── ports/                           # Domain Ports (Secondary)
│   │   ├── conversation_repository.py   # 대화 저장소
│   │   ├── query_understanding_service_port.py  # 질의 이해 서비스
│   │   ├── search_service_port.py       # 검색 서비스
│   │   ├── suggestion_service_port.py   # 연관질문 서비스
│   │   └── document_upload_service_port.py # 문서 업로드 서비스
│   └── events/
│       ├── query_received.py            # 질의 수신 이벤트
│       └── answer_generated.py          # 답변 생성 이벤트
├── application/
│   ├── ports/
│   │   ├── primary/
│   │   │   ├── chat_service_port.py     # 채팅 서비스 (Primary Port)
│   │   │   ├── suggestion_service_port.py # 연관질문 서비스 (Primary Port)
│   │   │   └── upload_service_port.py   # 업로드 서비스 (Primary Port)
│   │   └── secondary/                   # Infrastructure Ports (Secondary)
│   │       ├── llm_service_port.py      # LLM 서비스
│   │       ├── vector_search_port.py    # 벡터 검색 서비스
│   │       └── embedding_service_port.py # 임베딩 서비스
│   ├── use_cases/
│   │   ├── process_chat_use_case.py     # 채팅 처리 Use Case
│   │   ├── generate_suggestion_use_case.py # 연관질문 생성 Use Case
│   │   └── upload_document_use_case.py  # 문서 업로드 Use Case
│   ├── commands/
│   │   ├── chat_command.py              # 채팅 명령
│   │   ├── suggestion_command.py        # 연관질문 명령
│   │   └── upload_command.py            # 업로드 명령
│   └── responses/
│       ├── chat_response_dto.py         # 채팅 응답 DTO
│       ├── suggestion_response_dto.py   # 연관질문 응답 DTO
│       └── upload_response_dto.py       # 업로드 응답 DTO
├── infrastructure/
│   └── adapters/
│       ├── primary/
│       │   └── web/
│       │       ├── __init__.py
│       │       ├── common/                     # 공통 라이브러리
│       │       │   ├── __init__.py
│       │       │   ├── base_schemas.py         # 공통 베이스 스키마
│       │       │   ├── validators.py           # 공통 검증 로직
│       │       │   ├── response_builders.py    # 공통 응답 빌더
│       │       │   ├── decorators.py           # 공통 데코레이터
│       │       │   └── exceptions.py           # 공통 예외 처리
│       │       ├── chat/                       # 채팅 전용
│       │       │   ├── __init__.py
│       │       │   ├── chat_controller.py      # 채팅 컨트롤러
│       │       │   └── schemas/
│       │       │       ├── __init__.py
│       │       │       ├── request_schema.py   # 채팅 요청 스키마
│       │       │       └── response_schema.py  # 채팅 응답 스키마
│       │       ├── suggestion/                 # 연관질문 전용
│       │       │   ├── __init__.py
│       │       │   ├── suggestion_controller.py # 연관질문 컨트롤러
│       │       │   └── schemas/
│       │       │       ├── __init__.py
│       │       │       ├── request_schema.py   # 연관질문 요청 스키마
│       │       │       └── response_schema.py  # 연관질문 응답 스키마
│       │       └── upload/                     # 업로드 전용
│       │           ├── __init__.py
│       │           ├── upload_controller.py    # 업로드 컨트롤러
│       │           └── schemas/
│       │               ├── __init__.py
│       │               ├── request_schema.py   # 업로드 요청 스키마
│       │               └── response_schema.py  # 업로드 응답 스키마
│       └── secondary/
│           ├── elasticsearch/
│           │   ├── elasticsearch_connection.py
│           │   ├── elasticsearch_search_adapter.py
│           │   └── elasticsearch_models.py
│           ├── llm/
│           │   ├── langchain_llm_adapter.py
│           │   ├── query_understanding_adapter.py
│           │   └── embedding_adapter.py
│           └── memory/
│               └── in_memory_conversation_repository.py
└── configuration/
    ├── di_container.py                  # 의존성 주입 컨테이너
    ├── settings/
    │   ├── app_settings.py              # 애플리케이션 설정
    │   ├── constants.py                 # 상수
    │   └── environment_config.py        # 환경별 설정
    ├── web/
    │   ├── app_factory.py               # FastAPI 앱 팩토리
    │   ├── middleware_config.py         # 미들웨어 설정
    │   └── router_registry.py           # 라우터 등록
    └── startup/
        └── bootstrap.py                 # 애플리케이션 부트스트랩

```

## 핵심 설계 원칙 적용
### 1. Domain Layer 설계
**Thread (Aggregate Root)**:
- 대화 세션을 관리하는 애그리게이트 루트
- 메시지 추가, 의도 분류, 답변 생성 등의 비즈니스 로직 포함

**Message (Entity)**:
- 각 대화 메시지를 나타내는 엔티티
- 사용자 질의와 봇 응답을 구분

**SearchIntent (Value Object)**:
- FAQ, VDB, 재질의 의도 분류 결과
- 신뢰도 점수와 이유 포함

### 2. Port 설계
**Primary Port**:
- `ChatServicePort`: 채팅 처리의 주요 인터페이스

**Domain Ports** (Secondary):
- `ConversationRepository`: 대화 데이터 저장
- `QueryUnderstandingServicePort`: 질의 이해 및 분해
- `SearchServicePort`: 문서 검색

**Infrastructure Ports** (Secondary):
- `LLMServicePort`: LLM 호출
- `VectorSearchPort`: 벡터 검색
- `EmbeddingServicePort`: 텍스트 임베딩

### 3. Use Case 설계
`ProcessChatUseCase`가 전체 워크플로우를 오케스트레이션:
1. 사용자 질의 수신
2. 질의 재작성 및 분해
3. 의도 분류
4. 적절한 검색 전략 실행
5. LLM을 통한 답변 생성
6. 응답 반환

### 4. Adapter 설계
**Primary Adapter**:
- `ChatController`: FastAPI 기반 REST API 엔드포인트

**Secondary Adapters**:
- `ElasticsearchSearchAdapter`: 하이브리드 검색 구현
- `LangChainLLMAdapter`: LangChain 기반 LLM 서비스
- `QueryUnderstandingAdapter`: 질의 이해 로직 구현

## 주요 특징
1. **단일 책임**: 각 컴포넌트가 명확한 역할을 가짐
2. **기술 분리**: Elasticsearch, LangChain 등 기술적 세부사항은 어댑터에서 처리
3. **확장성**: 새로운 검색 엔진이나 LLM 모델로 쉽게 교체 가능
4. **테스트 용이성**: 포트를 통한 모킹으로 단위 테스트 가능
5. **인터페이스 준수**: 제공된 API 명세를 정확히 구현
