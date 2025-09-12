# LotteCard-Search  
롯데카드 프로젝트 - LOCA앱, 사내지식 검색  
  
## 설계 전략 DDD + Hexagonal  
### DDD 구성요소  
1. Aggregate Root  
  - 비즈니스 핵심 개체이면서 일관성 경계를 관리  
  - 고유 식별자를 가지고 라이프사이클을 독립적으로 관리  
2. Entity  
  - 고유 식별자를 가지지만 Aggregate에 종속  
  - 상태 변화를 추적해야 하는 객체  
3. Value Object(VO)  
  - 불변 객체이며 식별자가 없음  
  - 값 자체가 의미를 가지는 객체  
4. Domain Service  
  - 복잡한 비즈니스 로직이나 여러 Aggregate 간 조율  
  - 무상태 서비스  
5. Repository  
  - 데이터 접근 추상화  
  - Aggregate 영속성 관리  
6. Domain Events: 도메인 간 비동기 통신  
7. Factories: 복잡한 객체 생성 로직  
  
# LOCA앱 통합 챗봇 - 강화된 DDD 구성요소별 프로그램 분류

## 설계 전략 DDD + Hexagonal Architecture

### 헥사고날 아키텍처 레이어 정의
1. **Domain Layer**: 순수 비즈니스 로직 (Aggregate, Entity, Value Object, Domain Service)
2. **Application Layer**: Use Case 조율 및 Port 인터페이스 정의
3. **Interface Layer**: Primary Adapter (REST API, CLI, Event Listener)
4. **Infrastructure Layer**: Secondary Adapter (Database, External API, Cache)

## 도메인별 상세 분류

### 🤖 Agent Domain (Core Domain)

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-011 | Supervisor Agent 프로그램 | **Aggregate Root** | Domain | 전체 검색 워크플로우를 조율하는 메인 컨트롤러 | 가장 핵심적인 비즈니스 객체 |
| PGM-RTV-012 | Query Planning 프로그램 | **Domain Service** | Domain | 질의 목적 및 인덱스 종류에 따른 최적 검색 계획 수립 | 복잡한 계획 수립 로직 |
| PGM-RTV-013 | Query Replanner 프로그램 | **Domain Service** | Domain | 검색 결과 검증 및 동적 재계획 수행 (최대 3회) | 적응적 의사결정 로직 |
| PGM-RTV-015 | Card Worker 프로그램 | **Entity** | Domain | 카드 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |
| PGM-RTV-016 | 상품공시실 Worker 프로그램 | **Entity** | Domain | 상품공시실 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |
| PGM-RTV-017 | 이벤트 Worker 프로그램 | **Entity** | Domain | 이벤트 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |
| PGM-RTV-018 | 컨텐츠 Worker 프로그램 | **Entity** | Domain | 컨텐츠 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |
| PGM-RTV-019 | 메뉴 Worker 프로그램 | **Entity** | Domain | 메뉴 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |
| PGM-RTV-020 | 커머스 Worker 프로그램 | **Entity** | Domain | 커머스 인덱스 전문 검색 에이전트 | Worker Agent의 구체 구현 |

### 🔍 RAG Pipeline Domain (Supporting Domain)

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-014 | HybridSearch 프로그램 | **Domain Service** | Domain | ElasticSearch 키워드 + Sparse + Dense Vector 검색 | 검색 알고리즘 조율 |
| PGM-RTV-021 | 문서 재정렬 프로그램 | **Domain Service** | Domain | LLM/Cross-Encoder 기반 검색 결과 재정렬 | 복잡한 랭킹 로직 |
| PGM-RTV-022 | 카드 혜택 기반 리랭킹 프로그램 | **Domain Service** | Domain | 카드 인덱스 검색 결과의 혜택 기준 재정렬 | 도메인 특화 랭킹 |
| PGM-RTV-023 | 결과 검증 프로그램 | **Domain Service** | Domain | Hallucination 최소화 및 신뢰성 검증 | 품질 관리 로직 |

### 🎨 Answer Domain (Core Domain) - 신규 추가

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-024 | 문서 기반 생성 프로그램 | **Domain Service** | Domain | 검색된 문서와 컨텍스트를 활용한 응답 생성 | 핵심 응답 생성 로직 |
| PGM-RTV-025 | 템플릿 분류 프로그램 | **Domain Service** | Domain | 질의 유형에 따른 최적 응답 템플릿 선택 | 템플릿 선택 알고리즘 |
| PGM-RTV-026 | 템플릿 기반 생성 프로그램 | **Domain Service** | Domain | 선택된 템플릿과 검색 결과 기반 최종 답변 생성 | 템플릿 기반 생성 엔진 |
| PGM-RTV-030 | 연관 검색 및 추천 프로그램 | **Domain Service** | Domain | 사용자 질의와 유사한 연관 검색어 생성 및 추천 | 개인화 추천 로직 |

### 💬 Conversation Domain (Supporting Domain) - 신규 추가

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-031 | 채팅 히스토리 관리 프로그램 | **Domain Service** | Domain | Redis 기반 대화 이력 저장 및 조회 관리 | 컨텍스트 유지 및 개인화 |

### 🛡️ Security Domain (Generic Domain)

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-002 | 개인정보 감지 프로그램 (Input) | **Domain Service** | Domain | 입력에서 개인정보 실시간 감지 및 마스킹 | 입력 보안 정책 |
| PGM-RTV-003 | 금지어 감지 프로그램 (Input) | **Domain Service** | Domain | 입력에서 부적절 질문 식별 및 차단 | 입력 콘텐츠 필터링 |
| PGM-RTV-004 | 프롬프트 인젝션 감지 프로그램 | **Domain Service** | Domain | 비정상적 검색 패턴 탐지 및 차단 | 보안 공격 방어 |
| PGM-RTV-005 | Rate Limiting 프로그램 | **Domain Service** | Domain | 반복적/자동화된 요청 감지 및 제한 | 시스템 보호 |
| PGM-RTV-027 | 개인정보 감지 프로그램 (Output) | **Domain Service** | Domain | 출력에서 개인정보 실시간 감지 및 마스킹 | 출력 보안 정책 |
| PGM-RTV-028 | 금지어 감지 프로그램 (Output) | **Domain Service** | Domain | 출력에서 부적절 내용 식별 및 차단 | 출력 콘텐츠 필터링 |
| PGM-RTV-029 | 편향 감지 프로그램 | **Domain Service** | Domain | 편향적 응답 탐지 및 차단 | AI 윤리 관리 |

### 🔤 Query Processing Domain (Supporting Domain)

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-006 | 쿼리 재작성 프로그램 | **Domain Service** | Domain | LLM 활용 검색 최적화 질의 변환 | 쿼리 최적화 |
| PGM-RTV-007 | 쿼리 분해 프로그램 | **Domain Service** | Domain | 복잡한 질문을 단순한 하위 질문으로 분해 | 쿼리 구조화 |
| PGM-RTV-008 | 엔티티 추출 프로그램 | **Domain Service** | Domain | 재작성된 쿼리에서 엔티티 추출 | NER 로직 |
| PGM-RTV-009 | 질의 목적 분류 프로그램 | **Domain Service** | Domain | 재작성된 쿼리의 질의 목적 분류 | 의도 분류 |
| PGM-RTV-010 | 예외성 답변 처리 프로그램 | **Domain Service** | Domain | FAQ 또는 재질의 기능을 통한 예외 상황 처리 | 컴플라이언스 및 예외 처리 |

### 🎮 Application Layer

| 프로그램 ID | 프로그램명 | DDD 구성요소 | 레이어 | 설명 | 비고 |
|------------|-----------|-------------|-------|------|------|
| PGM-RTV-001 | 챗봇 수행 API 프로그램 | **Use Case** | Application | LOCA앱 연동 API 및 전체 프로세스 조율 | FastAPI 엔드포인트 |

## 강화된 구성요소 정의

### 💎 핵심 Value Objects (완전한 목록)

| 구성요소 | 도메인 | 설명 | 관련 프로그램 |
|---------|--------|------|-------------|
| **ExecutionPlan** | Agent | 검색 실행 계획 (전략, 순서, 임계값) | PGM-RTV-012, 013 |
| **SearchParameters** | RAG | 검색 파라미터 (top_k, threshold, filters) | PGM-RTV-014 |
| **SecurityRule** | Security | 보안 규칙 (패턴, 액션, 심각도) | PGM-RTV-002~005, 027~029 |
| **QueryIntent** | Query | 질의 의도 (목적, 신뢰도) | PGM-RTV-009 |
| **RankingScore** | RAG | 랭킹 점수 (관련성, 인기도, 최신성) | PGM-RTV-021, 022 |
| **AnswerTemplate** | Answer | 응답 템플릿 (타입, 프롬프트, 제약사항) | PGM-RTV-025, 026 |
| **BrandGuideline** | Answer | 브랜드 가이드라인 (톤, 스타일, 규칙) | PGM-RTV-024~026 |
| **ConversationContext** | Conversation | 대화 컨텍스트 (이력, 선호도, 상태) | PGM-RTV-031 |
| **UserPermission** | Security | 사용자 권한 (역할, 접근 범위, 제한) | PGM-RTV-014 |
| **EntityType** | Query | 엔티티 유형 (도메인별 분류 및 속성) | PGM-RTV-008 |

### 🏗️ 핵심 Aggregate Roots

| Aggregate Root | 도메인 | 책임 | 불변성 규칙 |
|---------------|--------|------|------------|
| **SupervisorAgent** | Agent | 검색 워크플로우 전체 조율 | 동시에 하나의 실행 계획만 활성화 |
| **ConversationSession** | Conversation | 사용자 대화 세션 관리 | 세션당 사용자는 유일하며 순차적 메시지 보장 |
| **SecurityPolicy** | Security | 보안 정책 및 규칙 관리 | 정책 변경 시 모든 규칙의 일관성 보장 |
| **AnswerTemplate** | Answer | 템플릿 및 브랜드 가이드라인 관리 | 템플릿 버전 간 호환성 보장 |
| **UserQuery** | Query | 사용자 질의 및 처리 상태 관리 | 처리 단계의 순차성 보장 |

### 📊 Entity 세부 분류

| Entity | 부모 Aggregate | 식별자 | 주요 속성 | 상태 변화 |
|--------|---------------|--------|----------|----------|
| **WorkerAgent** | SupervisorAgent | worker_id | 타입, 성능지표, 부하상태 | 유휴→실행→완료→유휴 |
| **Message** | ConversationSession | message_id | 타입, 내용, 타임스탬프 | 생성→전송→확인 |
| **GuardrailResult** | SecurityPolicy | result_id | 위반사항, 조치내역 | 탐지→처리→로깅 |
| **ProcessedQuery** | UserQuery | query_id | 재작성내용, 엔티티, 의도 | 원본→처리→검증→완료 |
| **RetrievalResult** | SearchContext | result_id | 관련성점수, 출처, 내용 | 검색→랭킹→검증 |

### 🗄️ Repository Interfaces (완전한 목록)

| Repository | 도메인 | 책임 | 주요 메서드 |
|-----------|--------|------|------------|
| **AgentRepository** | Agent | Agent 상태 및 실행 이력 관리 | save, findById, findActiveAgents |
| **DocumentRepository** | RAG | 문서 및 검색 결과 캐싱 | save, findByQuery, findByIndex |
| **QueryHistoryRepository** | Query | 쿼리 이력 및 패턴 분석 | save, findByUser, analyzePatterns |
| **SecurityLogRepository** | Security | 보안 이벤트 로깅 및 분석 | log, findViolations, generateReport |
| **AnswerTemplateRepository** | Answer | 응답 템플릿 관리 및 버전 제어 | save, findByType, getActiveVersion |
| **ConversationRepository** | Conversation | 대화 이력 저장 및 조회 | save, findByThreadId, findByUser |
| **UserProfileRepository** | Shared | 사용자 프로필 및 선호도 관리 | save, findByUserId, updatePreferences |

### 📡 Domain Events (완전한 목록)

| Event | 발생 조건 | 페이로드 | 구독자 | 처리 방식 |
|-------|----------|---------|--------|----------|
| **PlanAssignedEvent** | Supervisor Agent 계획 수립 | agent_id, plan_id, strategy | Monitoring Service | 비동기 |
| **ExecutionStartedEvent** | Agent 실행 개시 | agent_id, estimated_time | Performance Tracker | 비동기 |
| **ReplanningTriggeredEvent** | 검색 결과 품질 미달 | agent_id, failure_reason, attempt | Quality Analyzer | 비동기 |
| **TaskCompletedEvent** | Worker Agent 작업 완료 | worker_id, performance_metrics | Result Aggregator | 비동기 |
| **SecurityThreatDetectedEvent** | 가드레일 규칙 위배 | threat_type, severity, user_id | Security Monitor | 즉시 |
| **QueryProcessedEvent** | NLU 파이프라인 완료 | query_id, processing_time, entities | Analytics Service | 비동기 |
| **AnswerGeneratedEvent** | 답변 생성 완료 | answer_id, quality_score, template_used | Quality Evaluator | 비동기 |
| **ConversationStartedEvent** | 새 대화 세션 시작 | thread_id, user_id | Personalization Service | 비동기 |
| **TemplateUpdatedEvent** | 템플릿 수정 완료 | template_id, version, changes | Cache Invalidator | 즉시 |

### 🏭 Factories (완전한 목록)

| Factory | 책임 | 생성 복잡도 | 검증 규칙 |
|---------|------|------------|----------|
| **SupervisorAgentFactory** | SupervisorAgent + 초기 컨텍스트 생성 | 높음 | 사용 가능한 Worker 검증 |
| **WorkerAgentFactory** | 인덱스별 전문 Worker Agent 생성 | 중간 | 인덱스 타입별 설정 검증 |
| **ExecutionPlanFactory** | 쿼리 분석 기반 최적 계획 생성 | 높음 | 리소스 제약사항 검증 |
| **SearchContextFactory** | 파라미터 검증된 검색 컨텍스트 생성 | 중간 | 권한 및 필터 검증 |
| **SecurityPolicyFactory** | 규칙 조합된 보안 정책 생성 | 중간 | 규칙 충돌 검증 |
| **AnswerTemplateFactory** | 브랜드 가이드라인 적용 템플릿 생성 | 높음 | 브랜드 일관성 검증 |
| **ConversationSessionFactory** | 사용자별 대화 세션 생성 | 낮음 | 중복 세션 방지 |

## 헥사곤 간 의존성 관리

### Port 인터페이스 정의

**Inbound Ports (Primary)**
- ChatbotService: 챗봇 주요 기능 인터페이스
- AgentManagementService: Agent 관리 인터페이스
- ConversationService: 대화 관리 인터페이스
- SecurityMonitoringService: 보안 모니터링 인터페이스

**Outbound Ports (Secondary)**
- LLMService: 외부 LLM API 호출
- SearchEngineService: 검색 엔진 연동
- CacheService: 캐시 시스템 연동
- NotificationService: 알림 시스템 연동

### 의존성 역전 원칙 적용

```
Domain ← Application ← Interface
   ↑         ↑           ↑
   └─── Infrastructure ─┘
```

- Domain은 어떤 외부 의존성도 갖지 않음
- Application은 Domain 및 Port 인터페이스에만 의존
- Infrastructure는 Port 인터페이스를 구현
- Interface는 Application Use Case를 호출

## 품질 속성 고려사항

### 성능 (Performance)
- Agent 병렬 처리로 응답 시간 최적화
- 캐시 전략으로 반복 요청 처리 시간 단축
- 비동기 이벤트 처리로 시스템 처리량 향상

### 확장성 (Scalability)
- 도메인별 독립적 확장 가능
- Worker Agent 동적 스케일링
- 메시지 큐 기반 이벤트 처리

### 보안성 (Security)
- 다층 가드레일 시스템
- 실시간 위협 탐지 및 대응
- 감사 로그 및 추적 기능

### 유지보수성 (Maintainability)
- 도메인별 독립적 개발 및 배포
- 명확한 책임 분리
- 테스트 용이성 확보

이 강화된 설계로 LOCA앱 통합 챗봇은 확장 가능하고 유지보수가 용이한 시스템이 될 것입니다.
  
### **Aggregate Root 선정 기준**  
- ✅ **독립적 라이프사이클** 관리  
- ✅ **비즈니스 불변성** 보장  
- ✅ **트랜잭션 경계** 역할  
  
### **Domain Service 선정 기준**  - ✅ **복잡한 비즈니스 로직** 포함  
- ✅ **여러 객체 간 조율** 필요  
- ✅ **상태를 갖지 않는** 순수 로직  
  
### **Entity vs Value Object 구분**  
- **Entity**: 식별자가 중요하고 상태 변화 추적 필요  
- **Value Object**: 값 자체가 의미이며 불변성 유지  
  
### **도메인 우선순위 재정의**  
1. **Core Domain**: Agent, Response (기업 핵심 경쟁력 및 차별화 요소)  
2. **Supporting Domain**: RAG, Query (핵심 비즈니스를 지원하는 전문 영역)  
3. **Generic Domain**: Security (범용적이지만 필수적인 기능)  
  
## 🚀 Response Domain 분리 효과  
  
### **비즈니스 가치**  
- **브랜드 일관성** 유지 및 강화  
- **고객 경험** 개선 및 만족도 향상  
- **컴플라이언스** 리스크 감소  
- **다국가 진출** 시 현지화 용이성  
  
### **기술적 이점**  
- **템플릿 관리**의 독립적 진화  
- **A/B 테스트** 및 성능 최적화  
- **전문팀 운영** (UX Writing, Brand, Localization)  
- **실시간 템플릿 업데이트** 가능  
  
이렇게 Response Domain을 분리함으로써 **기업의 핵심 가치**인 **고품질 응답 서비스**를 **체계적으로 관리**할 수 있게 되었습니다.  
  
  
  
- 구성도  
``` shell
src/
├── domain/                         # 🎯 순수 비즈니스 로직만
│   ├── agent/                      # Agent 도메인 (Core Domain)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── supervisor_agent.py     # Supervisor Agent Aggregate Root
│   │   │   ├── worker_agent.py         # Worker Agent Aggregate Root  
│   │   │   ├── planning_agent.py       # Planning Agent Aggregate Root
│   │   │   ├── execution_plan.py       # 실행 계획 Value Object
│   │   │   ├── conversation_context.py # 대화 컨텍스트 Value Object
│   │   │   └── search_task.py          # 검색 태스크 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── agent_planning_domain_service.py     # 복잡한 계획 수립 로직
│   │   │   ├── execution_strategy_service.py        # 실행 전략 결정 로직
│   │   │   └── agent_coordination_domain_service.py # Agent 간 조율 로직
│   │   ├── factories/
│   │   │   ├── supervisor_agent_factory.py
│   │   │   ├── worker_agent_factory.py
│   │   │   └── execution_plan_factory.py
│   │   └── events/
│   │       ├── plan_assigned_event.py
│   │       ├── execution_started_event.py
│   │       ├── replanning_triggered_event.py
│   │       ├── task_completed_event.py
│   │       └── execution_completed_event.py
│   ├── rag/                        # RAG 파이프라인 도메인 (Supporting Domain)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── search_context.py       # 검색 컨텍스트 Aggregate Root
│   │   │   ├── retrieval_result.py     # 검색 결과 Entity
│   │   │   ├── document.py             # 문서 Aggregate Root
│   │   │   ├── ranking_score.py        # 랭킹 점수 Value Object
│   │   │   ├── search_parameters.py    # 검색 파라미터 Value Object
│   │   │   ├── document_metadata.py    # 문서 메타데이터 Value Object
│   │   │   └── user_permission.py      # 사용자 권한 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── hybrid_search_algorithm_service.py   # PGM-RTV-015: 하이브리드 검색 로직
│   │   │   ├── ranking_algorithm_service.py         # PGM-RTV-022: 문서 재정렬 로직
│   │   │   ├── card_benefit_ranking_service.py      # PGM-RTV-023: 카드 혜택 랭킹
│   │   │   ├── relevance_calculation_service.py     # 관련성 계산 로직
│   │   │   ├── permission_filter_service.py         # 권한 기반 필터링
│   │   │   └── result_validation_domain_service.py  # PGM-RTV-024: 결과 검증 로직
│   │   ├── factories/
│   │   │   ├── search_context_factory.py
│   │   │   ├── document_factory.py
│   │   │   └── ranking_score_factory.py
│   │   └── events/
│   │       ├── retrieval_result_added_event.py
│   │       ├── reranking_applied_event.py
│   │       ├── document_indexed_event.py
│   │       ├── document_updated_event.py
│   │       └── search_completed_event.py
│   ├── answer/                     # 🆕 Answer 도메인 (Core Domain) - Response → Answer 변경
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── answer_template.py      # 답변 템플릿 Aggregate Root
│   │   │   ├── generated_answer.py     # 생성된 답변 Aggregate Root  
│   │   │   ├── template_category.py    # 템플릿 카테고리 Entity
│   │   │   ├── answer_context.py       # 답변 컨텍스트 Entity
│   │   │   ├── template_version.py     # 템플릿 버전 Entity
│   │   │   ├── related_suggestion.py   # 연관 추천 Entity
│   │   │   ├── answer_quality.py       # 답변 품질 Value Object
│   │   │   ├── template_metadata.py    # 템플릿 메타데이터 Value Object
│   │   │   ├── localization_info.py    # 다국어 정보 Value Object
│   │   │   ├── brand_guideline.py      # 브랜드 가이드라인 Value Object
│   │   │   ├── compliance_rule.py      # 컴플라이언스 규칙 Value Object
│   │   │   └── source_citation.py      # 출처 인용 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── document_based_generation_service.py # PGM-RTV-025: 문서 기반 생성
│   │   │   ├── template_selection_service.py        # PGM-RTV-026: 템플릿 선택 로직
│   │   │   ├── template_based_generation_service.py # PGM-RTV-027: 템플릿 기반 생성
│   │   │   ├── related_search_service.py            # PGM-RTV-032: 연관 검색 생성
│   │   │   ├── template_optimization_service.py     # 템플릿 최적화 로직
│   │   │   ├── brand_compliance_service.py          # 브랜드 준수 검증 로직
│   │   │   ├── answer_quality_service.py            # 답변 품질 평가 로직
│   │   │   ├── template_versioning_service.py       # 템플릿 버전 관리 로직
│   │   │   ├── localization_service.py              # 다국어 처리 로직
│   │   │   └── citation_management_service.py       # 출처 관리 로직
│   │   ├── factories/
│   │   │   ├── answer_template_factory.py
│   │   │   ├── generated_answer_factory.py
│   │   │   ├── template_category_factory.py
│   │   │   ├── answer_context_factory.py
│   │   │   └── related_suggestion_factory.py
│   │   └── events/
│   │       ├── template_selected_event.py
│   │       ├── answer_generated_event.py
│   │       ├── template_updated_event.py
│   │       ├── quality_evaluated_event.py
│   │       ├── brand_violation_detected_event.py
│   │       ├── localization_applied_event.py
│   │       └── related_suggestions_generated_event.py
│   ├── conversation/               # 🆕 Conversation 도메인 (Supporting Domain) - 새로 추가
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── conversation_session.py # 대화 세션 Aggregate Root
│   │   │   ├── message.py              # 메시지 Entity
│   │   │   ├── conversation_context.py # 대화 컨텍스트 Entity
│   │   │   ├── user_profile.py         # 사용자 프로필 Entity
│   │   │   ├── conversation_metadata.py # 대화 메타데이터 Value Object
│   │   │   ├── message_type.py         # 메시지 타입 Value Object
│   │   │   ├── conversation_state.py   # 대화 상태 Value Object
│   │   │   └── retention_policy.py     # 보존 정책 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── conversation_management_service.py   # PGM-RTV-028: 대화 관리
│   │   │   ├── context_tracking_service.py          # 컨텍스트 추적 로직
│   │   │   ├── personalization_service.py           # 개인화 로직
│   │   │   ├── conversation_analytics_service.py    # 대화 분석 로직
│   │   │   └── retention_management_service.py      # 보존 관리 로직
│   │   ├── factories/
│   │   │   ├── conversation_session_factory.py
│   │   │   ├── message_factory.py
│   │   │   └── user_profile_factory.py
│   │   └── events/
│   │       ├── conversation_started_event.py
│   │       ├── message_added_event.py
│   │       ├── conversation_ended_event.py
│   │       ├── context_updated_event.py
│   │       └── retention_applied_event.py
│   ├── security/                   # 보안 & 가드레일 도메인 (Generic Domain)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── security_policy.py      # 보안 정책 Aggregate Root
│   │   │   ├── guardrail_result.py     # 가드레일 결과 Entity
│   │   │   ├── rate_limit_session.py   # Rate Limit 세션 Entity
│   │   │   ├── security_rule.py        # 보안 규칙 Value Object
│   │   │   ├── threat_detection.py     # 위협 탐지 Value Object
│   │   │   └── rate_limit_rule.py      # Rate Limit 규칙 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── input_guardrail_service.py           # PGM-RTV-002,003,004: 입력 가드레일
│   │   │   ├── output_guardrail_service.py          # PGM-RTV-029,030,031: 출력 가드레일
│   │   │   ├── rate_limiting_service.py             # PGM-RTV-005: Rate Limiting
│   │   │   ├── personal_info_detection_service.py   # 개인정보 탐지
│   │   │   ├── profanity_detection_service.py       # 금지어 탐지
│   │   │   ├── prompt_injection_detection_service.py # 프롬프트 인젝션 탐지
│   │   │   ├── bias_detection_service.py            # 편향 탐지
│   │   │   ├── threat_analysis_service.py           # 위협 분석 로직
│   │   │   ├── policy_evaluation_service.py         # 정책 평가 로직
│   │   │   └── risk_calculation_service.py          # 위험도 계산 로직
│   │   ├── factories/
│   │   │   ├── security_policy_factory.py
│   │   │   └── guardrail_result_factory.py
│   │   └── events/
│   │       ├── security_threat_detected_event.py
│   │       ├── rate_limit_exceeded_event.py
│   │       ├── content_blocked_event.py
│   │       └── security_policy_updated_event.py
│   ├── query/                      # 쿼리 이해 도메인 (Supporting Domain)
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user_query.py           # 사용자 쿼리 Aggregate Root
│   │   │   ├── processed_query.py      # 처리된 쿼리 Entity
│   │   │   ├── extracted_entity.py     # 추출된 엔티티 Entity
│   │   │   ├── query_decomposition.py  # 쿼리 분해 Entity
│   │   │   ├── exception_case.py       # 예외 처리 Entity
│   │   │   ├── query_intent.py         # 쿼리 의도 Value Object
│   │   │   ├── entity_type.py          # 엔티티 타입 Value Object
│   │   │   ├── compliance_check.py     # 컴플라이언스 체크 Value Object
│   │   │   └── normalization_rule.py   # 정규화 규칙 Value Object
│   │   ├── services/                   # Domain Service (순수 비즈니스 로직만)
│   │   │   ├── query_rewriting_service.py        # PGM-RTV-006: 쿼리 재작성
│   │   │   ├── query_decomposition_service.py    # PGM-RTV-007: 쿼리 분해
│   │   │   ├── entity_extraction_service.py      # PGM-RTV-008: 엔티티 추출
│   │   │   ├── intent_classification_service.py  # PGM-RTV-009: 의도 분류
│   │   │   ├── exception_handling_service.py     # PGM-RTV-010: 예외 처리
│   │   │   ├── query_complexity_analyzer.py      # 쿼리 복잡도 분석
│   │   │   ├── intent_inference_service.py       # 의도 추론 로직
│   │   │   ├── entity_relationship_service.py    # 엔티티 관계 분석
│   │   │   ├── compliance_evaluation_service.py  # 컴플라이언스 평가
│   │   │   └── normalization_service.py          # 문법 정규화 서비스
│   │   ├── factories/
│   │   │   ├── user_query_factory.py
│   │   │   ├── processed_query_factory.py
│   │   │   ├── entity_factory.py
│   │   │   └── exception_case_factory.py
│   │   └── events/
│   │       ├── query_received_event.py
│   │       ├── query_processed_event.py
│   │       ├── entity_extracted_event.py
│   │       ├── intent_classified_event.py
│   │       ├── exception_detected_event.py
│   │       └── compliance_violation_detected_event.py
│   └── shared/                     # 공유 도메인 객체
│       ├── __init__.py
│       ├── base/
│       │   ├── base_entity.py
│       │   ├── base_aggregate.py
│       │   ├── base_value_object.py
│       │   └── base_domain_service.py
│       ├── events/
│       │   ├── domain_event.py
│       │   ├── event_dispatcher.py
│       │   └── event_handler.py
│       ├── exceptions/
│       │   ├── domain_exception.py
│       │   ├── validation_exception.py
│       │   └── business_rule_exception.py
│       ├── specifications/
│       │   ├── specification.py
│       │   └── composite_specification.py
│       └── value_objects/
│           ├── identifier.py
│           ├── timestamp.py
│           ├── score.py
│           └── metric.py
├── application/                    # 🎯 Use Cases & Ports
│   ├── __init__.py
│   ├── use_cases/                  # Use Case (Application Service)
│   │   ├── chatbot_use_case.py                   # PGM-RTV-001 (Main API)
│   │   ├── agent_management_use_case.py          # PGM-RTV-011,013,014 로직
│   │   ├── query_processing_use_case.py          # PGM-RTV-006~010 로직
│   │   ├── search_orchestration_use_case.py      # PGM-RTV-015~021 로직
│   │   ├── result_processing_use_case.py         # PGM-RTV-022~024 로직
│   │   ├── answer_generation_use_case.py         # PGM-RTV-025~027,032 로직
│   │   ├── conversation_management_use_case.py   # PGM-RTV-028 로직
│   │   ├── security_monitoring_use_case.py       # PGM-RTV-002~005, 029~031 로직
│   │   └── analytics_use_case.py
│   ├── ports/                      # Port Interfaces
│   │   ├── inbound/               # Primary Ports (Use Case Interfaces)
│   │   │   ├── chatbot_service.py
│   │   │   ├── agent_management_service.py
│   │   │   ├── search_service.py
│   │   │   ├── answer_service.py              # Response → Answer 변경
│   │   │   ├── conversation_service.py        # 새로 추가
│   │   │   └── monitoring_service.py
│   │   └── outbound/              # Secondary Ports
│   │       ├── repositories/      # Repository Interfaces
│   │       │   ├── agent_repository.py
│   │       │   ├── document_repository.py
│   │       │   ├── query_history_repository.py
│   │       │   ├── security_log_repository.py
│   │       │   ├── search_result_repository.py
│   │       │   ├── answer_template_repository.py     # Response → Answer
│   │       │   ├── generated_answer_repository.py    # Response → Answer
│   │       │   ├── template_analytics_repository.py
│   │       │   ├── conversation_repository.py        # 새로 추가
│   │       │   └── message_repository.py             # 새로 추가
│   │       ├── external_services/ # External Service Interfaces
│   │       │   ├── llm_service.py
│   │       │   ├── vector_db_service.py
│   │       │   ├── search_engine_service.py
│   │       │   ├── translation_service.py
│   │       │   └── notification_service.py
│   │       └── infrastructure/    # Infrastructure Interfaces
│   │           ├── cache_service.py
│   │           ├── event_publisher.py
│   │           ├── metrics_collector.py
│   │           ├── content_delivery_service.py
│   │           └── session_storage_service.py        # 새로 추가
│   ├── commands/                   # CQRS Commands
│   │   ├── process_chat_query_command.py
│   │   ├── create_agent_plan_command.py
│   │   ├── execute_search_command.py
│   │   ├── generate_answer_command.py                # Response → Answer
│   │   ├── update_template_command.py
│   │   ├── evaluate_answer_quality_command.py        # Response → Answer
│   │   ├── start_conversation_command.py             # 새로 추가
│   │   └── save_message_command.py                   # 새로 추가
│   ├── queries/                    # CQRS Queries
│   │   ├── get_agent_status_query.py
│   │   ├── get_search_history_query.py
│   │   ├── get_performance_metrics_query.py
│   │   ├── get_template_analytics_query.py
│   │   ├── get_answer_quality_metrics_query.py       # Response → Answer
│   │   ├── get_conversation_history_query.py         # 새로 추가
│   │   └── get_user_context_query.py                 # 새로 추가
│   ├── handlers/
│   │   ├── command_handlers/
│   │   │   ├── process_chat_query_handler.py
│   │   │   ├── create_agent_plan_handler.py
│   │   │   ├── execute_search_handler.py
│   │   │   ├── generate_answer_handler.py            # Response → Answer
│   │   │   ├── update_template_handler.py
│   │   │   ├── evaluate_answer_quality_handler.py    # Response → Answer
│   │   │   ├── start_conversation_handler.py         # 새로 추가
│   │   │   └── save_message_handler.py               # 새로 추가
│   │   └── query_handlers/
│   │       ├── get_agent_status_handler.py
│   │       ├── get_search_history_handler.py
│   │       ├── get_performance_metrics_handler.py
│   │       ├── get_template_analytics_handler.py
│   │       ├── get_answer_quality_metrics_handler.py # Response → Answer
│   │       ├── get_conversation_history_handler.py   # 새로 추가
│   │       └── get_user_context_handler.py           # 새로 추가
│   └── dto/
│       ├── chat_request_dto.py
│       ├── chat_response_dto.py
│       ├── agent_status_dto.py
│       ├── template_dto.py
│       ├── answer_quality_dto.py                     # Response → Answer
│       ├── conversation_dto.py                       # 새로 추가
│       └── message_dto.py                            # 새로 추가
├── interfaces/                     # 🔌 Primary Adapters (Inbound)
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── chatbot_controller.py     # FastAPI Controllers
│   │   │   ├── agent_controller.py
│   │   │   ├── search_controller.py
│   │   │   ├── answer_controller.py      # Response → Answer 변경
│   │   │   ├── template_controller.py
│   │   │   ├── conversation_controller.py # 새로 추가
│   │   │   └── monitoring_controller.py
│   │   ├── middleware/
│   │   │   ├── security_middleware.py
│   │   │   ├── rate_limiting_middleware.py
│   │   │   ├── localization_middleware.py
│   │   │   ├── conversation_middleware.py # 새로 추가
│   │   │   └── logging_middleware.py
│   │   └── schemas/
│   │       ├── chat_schemas.py
│   │       ├── agent_schemas.py
│   │       ├── search_schemas.py
│   │       ├── answer_schemas.py         # Response → Answer
│   │       ├── template_schemas.py
│   │       └── conversation_schemas.py   # 새로 추가
│   ├── events/
│   │   ├── event_listeners.py
│   │   └── webhook_handlers.py
│   └── cli/
│       ├── agent_commands.py
│       ├── template_commands.py
│       ├── conversation_commands.py      # 새로 추가
│       └── admin_commands.py
└── infrastructure/                 # 🔧 Secondary Adapters (Outbound)
    ├── __init__.py
    ├── repositories/               # Repository 구현체들
    │   ├── __init__.py
    │   ├── mongodb/
    │   │   ├── mongodb_agent_repository.py
    │   │   ├── mongodb_document_repository.py
    │   │   ├── mongodb_query_history_repository.py
    │   │   ├── mongodb_security_log_repository.py
    │   │   ├── mongodb_answer_template_repository.py    # Response → Answer
    │   │   ├── mongodb_generated_answer_repository.py   # Response → Answer
    │   │   ├── mongodb_conversation_repository.py
    │   │   └── mongodb_message_repository.py
    │   ├── elasticsearch/
    │   │   ├── elasticsearch_search_repository.py
    │   │   ├── elasticsearch_document_repository.py
    │   │   └── elasticsearch_template_search_repository.py
    │   ├── redis/
    │   │   ├── redis_cache_repository.py
    │   │   ├── redis_rate_limit_repository.py
    │   │   ├── redis_template_cache_repository.py
    │   │   └── redis_conversation_cache_repository.py   # 새로 추가 (PGM-RTV-028)
    │   └── memory/
    │       ├── in_memory_agent_repository.py
    │       ├── in_memory_cache_repository.py
    │       ├── in_memory_template_repository.py
    │       └── in_memory_conversation_repository.py
    ├── external_services/          # 외부 서비스 어댑터
    │   ├── __init__.py
    │   ├── llm/
    │   │   ├── openai_adapter.py
    │   │   ├── anthropic_adapter.py
    │   │   └── huggingface_adapter.py
    │   ├── vector_db/
    │   │   ├── pinecone_adapter.py
    │   │   ├── weaviate_adapter.py
    │   │   └── chroma_adapter.py
    │   ├── search_engine/
    │   │   ├── elasticsearch_adapter.py
    │   │   └── opensearch_adapter.py
    │   ├── translation/
    │   │   ├── google_translate_adapter.py
    │   │   ├── aws_translate_adapter.py
    │   │   └── deepl_adapter.py
    │   ├── content_delivery/
    │   │   ├── aws_s3_adapter.py
    │   │   └── azure_blob_adapter.py
    │   └── notification/
    │       ├── slack_adapter.py
    │       ├── email_adapter.py
    │       └── webhook_adapter.py
    ├── config/
    │   ├── __init__.py
    │   ├── database_config.py
    │   ├── cache_config.py
    │   ├── external_service_config.py
    │   ├── localization_config.py
    │   └── conversation_config.py
    ├── persistence/
    │   ├── __init__.py
    │   ├── mongodb_connection.py
    │   ├── elasticsearch_connection.py
    │   └── redis_connection.py
    └── logging/
        ├── __init__.py
        ├── structured_logger.py
        ├── event_logger.py
        ├── template_usage_logger.py
        └── conversation_logger.py
```


# LotteCard-Search
롯데카드 프로젝트 - LOCA앱, 사내지식 검색

# 서비스 설계 
1. LOCA앱 통합 챗봇
2. LOCA앱 통합 검색
3. 사내지식 검색
4. LOCA앱 API 관리
5. 사내지식 API 관리


# 아키텍처 설계(초안, 작성 진행중)
``` 
LOCA-ChatBot/
├── domain/
│   ├── ports/
│   │   ├── input/                       # 🔵 Input Ports (Driving)
│   │   │   ├── __init__.py
│   │   │   ├── chatbot_use_case.py      # 채팅 처리 유스케이스 포트
│   │   │   ├── conversation_use_case.py # 대화 관리 유스케이스 포트
│   │   │   └── knowledge_search_use_case.py # 지식 검색 유스케이스 포트
│   │   └── output/                      # 🔴 Output Ports (Driven)
│   │       ├── __init__.py
│   │       ├── search_port.py           # 검색 서비스 포트
│   │       ├── llm_port.py              # LLM 서비스 포트
│   │       ├── vector_store_port.py     # 벡터 저장소 포트
│   │       ├── conversation_repository.py # 대화 저장소 포트
│   │       └── notification_port.py      # 알림 서비스 포트
│
├── application/                         # 🎯 Application Services
│   ├── services/
│   │   ├── chatbot_service.py           # Input Port 구현
│   │   └── conversation_service.py      # Input Port 구현
│
├── infrastructure/
│   ├── adapters/
│   │   ├── input/                       # 🔵 Input Adapters (Primary)
│   │   │   ├── web/
│   │   │   │   ├── fastapi_router.py    # REST API 어댑터
│   │   │   │   └── websocket_handler.py # WebSocket 어댑터
│   │   │   ├── cli/
│   │   │   │   └── command_handler.py   # CLI 어댑터
│   │   │   └── messaging/
│   │   │       └── kafka_consumer.py    # 메시지 큐 어댑터
│   │   └── output/                      # 🔴 Output Adapters (Secondary)
│   │       ├── search/
│   │       │   ├── web_search_adapter.py
│   │       │   └── vector_search_adapter.py
│   │       ├── llm/
│   │       │   ├── openai_adapter.py
│   │       │   └── anthropic_adapter.py
│   │       ├── persistence/
│   │       │   ├── redis_repository.py
│   │       │   └── postgres_repository.py
│   │       └── external/
│   │           ├── email_adapter.py
│   │           └── slack_adapter.py
```

``` bash
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── models/              # 데이터 모델 (SQLAlchemy/Pydantic)
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── user.py
│   ├── schemas/             # Pydantic 스키마 (API 입출력)
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── user.py
│   ├── services/            # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   └── ai_service.py
│   ├── repositories/        # 데이터 액세스 계층
│   │   ├── __init__.py
│   │   └── chat_repository.py
│   ├── api/                 # API 라우터
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── user.py
│   │   └── deps.py          # 의존성 주입
│   ├── core/                # 설정 및 공통 기능
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   └── utils/               # 유틸리티 함수
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── requirements.txt
└── .env
```

``` bash
fastapi-chatbot/
├── app/
│   ├── main.py                          # FastAPI 앱 진입점
│   ├── config.py                        # 설정 관리
│   └── container.py                     # DI 컨테이너
│
├── domain/                              # 🏛️ Core Domain (비즈니스 로직)
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── conversation.py              # 대화 엔티티
│   │   ├── message.py                   # 메시지 엔티티
│   │   └── document.py                  # 문서 엔티티
│   ├── services/
│   │   ├── __init__.py
│   │   ├── supervisor_agent.py          # 🤖 Supervisor Agent 핵심 로직
│   │   ├── conversation_manager.py      # 대화 상태 관리
│   │   └── response_generator.py        # 응답 생성 로직
│   └── ports/                           # 🔌 포트 (인터페이스)
│       ├── __init__.py
│       ├── search_port.py               # 검색 인터페이스
│       ├── llm_port.py                  # LLM 인터페이스
│       ├── vector_store_port.py         # 벡터 저장소 인터페이스
│       └── conversation_repository.py   # 대화 저장소 인터페이스
│
├── application/                         # 🎯 Application Layer
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chatbot_service.py           # 메인 챗봇 서비스
│   │   └── agent_orchestrator.py       # 에이전트 오케스트레이션
│   ├── dtos/
│   │   ├── __init__.py
│   │   ├── chat_request.py              # 채팅 요청 DTO
│   │   └── chat_response.py             # 채팅 응답 DTO
│   └── use_cases/
│       ├── __init__.py
│       ├── process_chat.py              # 채팅 처리 유스케이스
│       └── search_knowledge.py          # 지식 검색 유스케이스
│
├── infrastructure/                      # 🔧 Infrastructure Layer
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── web/                         # 🌐 Web 어댑터
│   │   │   ├── __init__.py
│   │   │   ├── fastapi_router.py        # FastAPI 라우터
│   │   │   └── middleware.py            # 미들웨어
│   │   ├── search/                      # 🔍 검색 어댑터
│   │   │   ├── __init__.py
│   │   │   ├── web_search_adapter.py    # 웹 검색 구현
│   │   │   ├── vector_search_adapter.py # 벡터 검색 구현
│   │   │   └── hybrid_search_adapter.py # 하이브리드 검색
│   │   ├── llm/                         # 🧠 LLM 어댑터
│   │   │   ├── __init__.py
│   │   │   ├── openai_adapter.py        # OpenAI API
│   │   │   ├── anthropic_adapter.py     # Anthropic API
│   │   │   └── local_llm_adapter.py     # 로컬 LLM
│   │   ├── vector_store/                # 📊 벡터 저장소 어댑터
│   │   │   ├── __init__.py
│   │   │   ├── pinecone_adapter.py      # Pinecone
│   │   │   ├── weaviate_adapter.py      # Weaviate
│   │   │   └── chroma_adapter.py        # ChromaDB
│   │   └── persistence/                 # 💾 영속성 어댑터
│   │       ├── __init__.py
│   │       ├── redis_conversation.py    # Redis 대화 저장소
│   │       └── postgres_conversation.py # PostgreSQL 저장소
│   ├── external/                        # 🌍 외부 서비스
│   │   ├── __init__.py
│   │   ├── serpapi_client.py            # SerpAPI 클라이언트
│   │   ├── tavily_client.py             # Tavily API 클라이언트
│   │   └── embedding_client.py          # 임베딩 서비스
│   └── config/
│       ├── __init__.py
│       ├── database.py                  # DB 설정
│       └── external_apis.py             # 외부 API 설정
│
├── tests/                               # 🧪 테스트
│   ├── __init__.py
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   │   ├── test_chatbot_flow.py
│   │   └── test_search_integration.py
│   └── fixtures/
│       ├── __init__.py
│       └── mock_adapters.py             # Mock 어댑터들
│
├── scripts/                             # 📝 스크립트
│   ├── setup_vector_db.py               # 벡터 DB 초기 설정
│   └── migrate_conversations.py         # 데이터 마이그레이션
│
├── requirements.txt                     # 📦 의존성
├── pyproject.toml                       # 프로젝트 설정
├── docker-compose.yml                   # 🐳 Docker 구성
├── Dockerfile
└── README.md


LOCA-ChatBot/
├── domain/
│   ├── ports/
│   │   ├── input/                       # 🔵 Input Ports (Driving)
│   │   │   ├── __init__.py
│   │   │   ├── chatbot_use_case.py      # 채팅 처리 유스케이스 포트
│   │   │   ├── conversation_use_case.py # 대화 관리 유스케이스 포트
│   │   │   └── knowledge_search_use_case.py # 지식 검색 유스케이스 포트
│   │   └── output/                      # 🔴 Output Ports (Driven)
│   │       ├── __init__.py
│   │       ├── search_port.py           # 검색 서비스 포트
│   │       ├── llm_port.py              # LLM 서비스 포트
│   │       ├── vector_store_port.py     # 벡터 저장소 포트
│   │       ├── conversation_repository.py # 대화 저장소 포트
│   │       └── notification_port.py      # 알림 서비스 포트
│
├── application/                         # 🎯 Application Services
│   ├── services/
│   │   ├── chatbot_service.py           # Input Port 구현
│   │   └── conversation_service.py      # Input Port 구현
│
├── infrastructure/
│   ├── adapters/
│   │   ├── input/                       # 🔵 Input Adapters (Primary)
│   │   │   ├── web/
│   │   │   │   ├── fastapi_router.py    # REST API 어댑터
│   │   │   │   └── websocket_handler.py # WebSocket 어댑터
│   │   │   ├── cli/
│   │   │   │   └── command_handler.py   # CLI 어댑터
│   │   │   └── messaging/
│   │   │       └── kafka_consumer.py    # 메시지 큐 어댑터
│   │   └── output/                      # 🔴 Output Adapters (Secondary)
│   │       ├── search/
│   │       │   ├── web_search_adapter.py
│   │       │   └── vector_search_adapter.py
│   │       ├── llm/
│   │       │   ├── openai_adapter.py
│   │       │   └── anthropic_adapter.py
│   │       ├── persistence/
│   │       │   ├── redis_repository.py
│   │       │   └── postgres_repository.py
│   │       └── external/
│   │           ├── email_adapter.py
│   │           └── slack_adapter.py
```


``` bash
📦app/
├── 📁agents/                 # 모든 에이전트 정의 (LLM 기반 구성)
│   ├── 📄supervisor.py       # 프롬프트 라우팅 및 분기 판단
│   ├── 📄rag_agent.py        # RAG 처리 전담 에이전트
│   ├── 📄web_agent.py        # Web 검색 전담
│   └── 📄tool_agent.py       # 계산, 메모리, 툴 수행 에이전트 등
│
├── 📁domain/                # 도메인 규칙 및 추상화
│   ├── 📁prompt/            # 프롬프트 템플릿
│   ├── 📁schema/            # DTO / 메시지 포맷
│   └── 📁policy/            # 역할 기반 라우팅 정책 등
│
├── 📁services/              # UseCase 로직: 검색, 요약, 정제
│   ├── 📄rag_service.py
│   ├── 📄web_search_service.py
│   └── 📄ranking_service.py
│
├── 📁infrastructure/        # 외부 시스템 연동
│   ├── 📁llm/               # OpenAI, HuggingFace, LangChain 등
│   ├── 📁search/           # Web scraping, Bing, Serper 등
│   ├── 📁vectordb/         # FAISS, Pinecone, Qdrant 등
│   └── 📁storage/          # S3, Local DB, PostgreSQL 등
│
├── 📁presentation/          # FastAPI 라우터 및 인터페이스
│   ├── 📁routers/
│   │   └── 📄chat.py
│   ├── 📁schemas/
│   │   └── 📄chat.py
│   └── 📄dependencies.py
│
├── 📁core/                  # 설정, 로깅, 공통 도구
│   ├── 📄config.py
│   ├── 📄logger.py
│   └── 📄di_container.py
│
├── 📄main.py                # FastAPI 앱 시작점
└── 📄run_agent_loop.py      # CLI 기반 Supervisor Loop or Background Job
```