from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    JWT_ALGORITHM: str = 'HS256'

    API_KEY: str


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
