from typing import Dict, Any

# from domain.ports.conversation_repository import ConversationRepository
# from domain.ports.query_understanding_service_port import QueryUnderstandingServicePort
# from domain.ports.search_service_port import SearchServicePort
# from application.ports.primary.chat_service_port import ChatServicePort
# from application.ports.secondary.llm_service_port import LLMServicePort
# from application.ports.secondary.vector_search_port import VectorSearchPort
# from application.ports.secondary.embedding_service_port import EmbeddingServicePort
# from application.use_cases.process_chat_use_case import ProcessChatUseCase
#
# from infrastructure.adapters.secondary.memory.in_memory_conversation_repository import InMemoryConversationRepository
# from infrastructure.adapters.secondary.llm.query_understanding_adapter import QueryUnderstandingAdapter
# from infrastructure.adapters.secondary.elasticsearch.elasticsearch_search_adapter import ElasticsearchSearchAdapter
# from infrastructure.adapters.secondary.llm.langchain_llm_adapter import LangChainLLMAdapter
# from infrastructure.adapters.secondary.llm.embedding_adapter import EmbeddingAdapter

from configuration.settings.app_settings import AppSettings
from configuration.factories.logger_factory import get_logger

logger = get_logger()


class DIContainer:
    def __init__(self, settings: AppSettings):
        self._settings = settings
        self._instances: Dict[str, Any] = {}

    def _get_or_create(self, key: str, factory_func):
        if key not in self._instances:
            self._instances[key] = factory_func()
        return self._instances[key]

    # # Domain Port Implementations
    # def conversation_repository(self) -> ConversationRepository:
    #     return self._get_or_create(
    #         "conversation_repository",
    #         lambda: InMemoryConversationRepository()
    #     )
    #
    # def query_understanding_service(self) -> QueryUnderstandingServicePort:
    #     return self._get_or_create(
    #         "query_understanding_service",
    #         lambda: QueryUnderstandingAdapter(
    #             llm_service=self.llm_service()
    #         )
    #     )
    #
    # def search_service(self) -> SearchServicePort:
    #     return self._get_or_create(
    #         "search_service",
    #         lambda: ElasticsearchSearchAdapter(
    #             settings=self._settings,
    #             embedding_service=self.embedding_service()
    #         )
    #     )
    #
    # # Infrastructure Port Implementations
    # def llm_service(self) -> LLMServicePort:
    #     return self._get_or_create(
    #         "llm_service",
    #         lambda: LangChainLLMAdapter(self._settings)
    #     )
    #
    # def vector_search_service(self) -> VectorSearchPort:
    #     return self._get_or_create(
    #         "vector_search_service",
    #         lambda: ElasticsearchSearchAdapter(
    #             settings=self._settings,
    #             embedding_service=self.embedding_service()
    #         )
    #     )
    #
    # def embedding_service(self) -> EmbeddingServicePort:
    #     return self._get_or_create(
    #         "embedding_service",
    #         lambda: EmbeddingAdapter(self._settings)
    #     )
    #
    # # Primary Port Implementation (Use Cases)
    # def chat_service(self) -> ChatServicePort:
    #     return self._get_or_create(
    #         "chat_service",
    #         lambda: ProcessChatUseCase(
    #             conversation_repository=self.conversation_repository(),
    #             query_understanding_service=self.query_understanding_service(),
    #             search_service=self.search_service(),
    #             llm_service=self.llm_service()
    #         )
    #     )


# Global container instance
_container: DIContainer = None

def get_container() -> DIContainer:
    global _container
    if _container is None:
        from configuration.settings.app_settings import get_settings
        _container = DIContainer(get_settings())
    return _container

def init_container(settings: AppSettings) -> None:
    global _container
    _container = DIContainer(settings)

async def cleanup_container() -> None:
    """DI 컨테이너 정리"""
    # 데이터베이스 연결 종료, 캐시 정리 등
    logger.info("DI Container cleanup completed")
