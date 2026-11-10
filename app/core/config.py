from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # 키가 없으면 서버는 가짜 LLM 클라이언트로 동작한다.
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-6-luna"
    openai_reasoning_effort: Literal["none", "minimal", "low", "medium", "high", "xhigh"] = "none"
    openai_max_output_tokens: int = Field(default=2000, gt=0)
    openai_timeout_seconds: float = Field(default=30.0, gt=0)

    fake_llm: bool = False
    fake_llm_delay_seconds: float = Field(default=1.0, ge=0)

@lru_cache
def get_settings() -> Settings:
    return Settings()
