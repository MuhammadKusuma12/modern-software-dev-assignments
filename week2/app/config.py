"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_settings() -> "Settings":
    return Settings()


class Settings:
    """Centralized app settings with sensible defaults."""

    def __init__(self) -> None:
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.db_path: str = os.getenv("DB_PATH", "")
