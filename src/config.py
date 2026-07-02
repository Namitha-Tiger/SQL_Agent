from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    llm_api_key: Optional[str] = None
    llm_model: str = os.getenv("TIGER_AI_GATEWAY_MODEL", "gpt-4.1-mini")
    llm_base_url: Optional[str] = os.getenv("TIGER_AI_GATEWAY_URL")
    llm_provider: str = os.getenv("TIGER_AI_GATEWAY_PROVIDER", "openai")
    mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
    mysql_port: int = int(os.getenv("MYSQL_PORT", "3306"))
    mysql_user: str = os.getenv("MYSQL_USER", "root")
    mysql_password: str = os.getenv("MYSQL_PASSWORD", "")
    mysql_database: str = os.getenv("MYSQL_DATABASE", "retail_agent_assignment")

    @property
    def has_llm_config(self) -> bool:
        return bool(self.llm_api_key or os.getenv("TIGER_AI_GATEWAY_API_KEY"))


def get_settings() -> Settings:
    return Settings(
        llm_api_key=os.getenv("TIGER_AI_GATEWAY_API_KEY"),
        llm_model=os.getenv("TIGER_AI_GATEWAY_MODEL", "gpt-4.1-mini"),
        llm_base_url=os.getenv("TIGER_AI_GATEWAY_URL",""),
        llm_provider=os.getenv("TIGER_AI_GATEWAY_PROVIDER", "openai"),
    )
