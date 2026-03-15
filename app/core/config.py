from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    title: str = Field(default="Backend-DocApp", alias="APP_NAME")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"], alias="CORS_ORIGINS"
    )
    port: str = Field(default="8000", alias="BASE_PORT")
    host: str = Field(default="0.0.0.0", alias="BASE_HOST")

    ollama_host: str = Field(default="https://ollama.com", alias="OLLAMA_HOST")
    ollama_model: str = Field(default="gpt-oss:120b-cloud", alias="OLLAMA_MODEL")
    ollama_timeout: int = Field(default=90, alias="OLLAMA_TIMEOUT")
    ollama_key: str = Field(alias="OLLAMA_API_KEY")



settings = Settings()
