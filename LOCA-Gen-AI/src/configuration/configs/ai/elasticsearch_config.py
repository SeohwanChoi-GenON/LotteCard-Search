"""
Elasticsearch 설정
"""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from ..._types import DeploymentEnvironment
from typing import Optional, Dict, Any, List


class ElasticsearchConfig(BaseSettings):
    """Elasticsearch 설정"""

    deployment_env: DeploymentEnvironment

    # Elasticsearch 연결
    elasticsearch_hosts: List[str] = Field(["localhost:9200"], env="LOCA_ES_HOSTS")
    elasticsearch_username: Optional[str] = Field(None, env="LOCA_ES_USERNAME")
    elasticsearch_password: Optional[str] = Field(None, env="LOCA_ES_PASSWORD")
    elasticsearch_use_ssl: bool = Field(False, env="LOCA_ES_USE_SSL")
    elasticsearch_verify_certs: bool = Field(True, env="LOCA_ES_VERIFY_CERTS")

    # 연결 설정
    connection_timeout: int = Field(10, env="LOCA_ES_CONNECTION_TIMEOUT")
    request_timeout: int = Field(30, env="LOCA_ES_REQUEST_TIMEOUT")
    max_retries: int = Field(3, env="LOCA_ES_MAX_RETRIES")
    retry_on_timeout: bool = Field(True, env="LOCA_ES_RETRY_ON_TIMEOUT")

    # 인덱스 설정
    index_prefix: str = Field("loca", env="LOCA_ES_INDEX_PREFIX")
    document_index: str = Field("documents", env="LOCA_ES_DOCUMENT_INDEX")
    chat_history_index: str = Field("chat_history", env="LOCA_ES_CHAT_HISTORY_INDEX")
    user_feedback_index: str = Field("user_feedback", env="LOCA_ES_USER_FEEDBACK_INDEX")

    # 검색 설정
    default_search_size: int = Field(10, env="LOCA_ES_DEFAULT_SEARCH_SIZE")
    max_search_size: int = Field(100, env="LOCA_ES_MAX_SEARCH_SIZE")
    min_score: float = Field(0.1, env="LOCA_ES_MIN_SCORE")

    # 하이브리드 검색 설정 (키워드 + 벡터)
    keyword_search_weight: float = Field(0.3, env="LOCA_ES_KEYWORD_WEIGHT")
    vector_search_weight: float = Field(0.7, env="LOCA_ES_VECTOR_WEIGHT")

    # 벡터 검색 설정
    vector_field_name: str = Field("embedding", env="LOCA_ES_VECTOR_FIELD_NAME")
    vector_dimension: int = Field(1536, env="LOCA_ES_VECTOR_DIMENSION")  # OpenAI embedding 차원
    similarity_metric: str = Field("cosine", env="LOCA_ES_SIMILARITY_METRIC")

    # 인덱스 관리
    number_of_shards: int = Field(1, env="LOCA_ES_NUMBER_OF_SHARDS")
    number_of_replicas: int = Field(0, env="LOCA_ES_NUMBER_OF_REPLICAS")
    refresh_interval: str = Field("1s", env="LOCA_ES_REFRESH_INTERVAL")

    # 배치 처리 설정
    bulk_size: int = Field(100, env="LOCA_ES_BULK_SIZE")
    bulk_timeout: int = Field(60, env="LOCA_ES_BULK_TIMEOUT")

    @field_validator('keyword_search_weight', 'vector_search_weight')
    @classmethod
    def validate_search_weights(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError('Search weights must be between 0.0 and 1.0')
        return v

    @field_validator('default_search_size')
    @classmethod
    def validate_search_size(cls, v, info):
        # Pydantic V2에서는 다른 필드값에 접근하기 어려우므로 기본 검증만 수행
        if v <= 0:
            raise ValueError('Default search size must be positive')
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 환경별 설정 조정
        self._adjust_for_environment()
        # 가중치 검증을 여기서 수행
        self._validate_weights()

    def _validate_weights(self):
        """검색 가중치 합계 검증"""
        total_weight = self.keyword_search_weight + self.vector_search_weight
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(f'Keyword and vector search weights must sum to 1.0, got {total_weight}')

        if self.default_search_size > self.max_search_size:
            raise ValueError(f'Default search size ({self.default_search_size}) cannot exceed max search size ({self.max_search_size})')

    def _adjust_for_environment(self):
        """환경별 Elasticsearch 설정 조정"""
        if self.deployment_env == DeploymentEnvironment.DEVELOPMENT:
            self.number_of_replicas = 0  # 개발에서는 replica 불필요
            self.refresh_interval = "1s"  # 즉시 검색 가능
            self.request_timeout = 60

        elif self.deployment_env == DeploymentEnvironment.LOCAL:
            self.elasticsearch_hosts = ["localhost:9200"]
            self.elasticsearch_use_ssl = False
            self.elasticsearch_verify_certs = False
            self.number_of_replicas = 0

        elif self.deployment_env == DeploymentEnvironment.PRODUCTION:
            self.elasticsearch_use_ssl = True
            self.elasticsearch_verify_certs = True
            self.number_of_replicas = 1  # 운영에서는 replica 설정
            self.refresh_interval = "30s"  # 운영에서는 성능을 위해 지연
            self.request_timeout = 15

    def get_elasticsearch_client_config(self) -> Dict[str, Any]:
        """Elasticsearch 클라이언트 설정 반환"""
        config = {
            "hosts": self.elasticsearch_hosts,
            "timeout": self.connection_timeout,
            "retry_on_timeout": self.retry_on_timeout,
            "max_retries": self.max_retries,
        }

        if self.elasticsearch_username and self.elasticsearch_password:
            config["basic_auth"] = (self.elasticsearch_username, self.elasticsearch_password)

        if self.elasticsearch_use_ssl:
            config["use_ssl"] = True
            config["verify_certs"] = self.elasticsearch_verify_certs

        return config

    def get_index_name(self, index_type: str) -> str:
        """인덱스 이름 생성"""
        index_map = {
            "document": self.document_index,
            "chat_history": self.chat_history_index,
            "user_feedback": self.user_feedback_index,
        }

        base_name = index_map.get(index_type, index_type)
        return f"{self.index_prefix}_{base_name}"

    def get_index_settings(self) -> Dict[str, Any]:
        """인덱스 기본 설정 반환"""
        return {
            "number_of_shards": self.number_of_shards,
            "number_of_replicas": self.number_of_replicas,
            "refresh_interval": self.refresh_interval,
        }

    def get_vector_mapping(self) -> Dict[str, Any]:
        """벡터 필드 매핑 설정 반환"""
        return {
            "type": "dense_vector",
            "dims": self.vector_dimension,
            "similarity": self.similarity_metric
        }

    def get_hybrid_search_config(self) -> Dict[str, Any]:
        """하이브리드 검색 설정 반환"""
        return {
            "keyword_weight": self.keyword_search_weight,
            "vector_weight": self.vector_search_weight,
            "min_score": self.min_score,
            "size": self.default_search_size
        }

    class Config:
        env_prefix = "LOCA_ES_"
        case_sensitive = False