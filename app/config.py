import os
from typing import Any


class Settings:
    """Simple environment-backed settings for local TrustAI development."""

    def __init__(self) -> None:
        self.app_name = os.getenv("TRUSTAI_APP_NAME", "TrustAI — AI Reliability Lab")
        self.environment = os.getenv("TRUSTAI_ENV", "development")
        self.database_url = os.getenv("TRUSTAI_DATABASE_URL", "sqlite:///./trustai.db")
        self.max_dataset_rows = int(os.getenv("TRUSTAI_MAX_DATASET_ROWS", "5000"))
        self.max_dataset_bytes = int(os.getenv("TRUSTAI_MAX_DATASET_BYTES", str(5 * 1024 * 1024)))
        self.log_level = os.getenv("TRUSTAI_LOG_LEVEL", "INFO")

    def model_dump(self) -> dict[str, Any]:
        return {
            "app_name": self.app_name,
            "environment": self.environment,
            "database_url": self.database_url,
            "max_dataset_rows": self.max_dataset_rows,
            "max_dataset_bytes": self.max_dataset_bytes,
            "log_level": self.log_level,
        }


settings = Settings()
