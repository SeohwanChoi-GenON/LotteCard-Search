"""데이터베이스 설정"""

from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """데이터베이스 설정"""

    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    database: str = Field(default="loca_db", env="DB_NAME")
    username: str = Field(default="loca_user", env="DB_USERNAME")
    password: str = Field(default="loca_password", env="DB_PASSWORD")

    class Config:
        env_file = ".env"
        extra = "ignore"


