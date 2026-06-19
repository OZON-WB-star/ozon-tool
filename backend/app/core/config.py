import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "dae-erp")
    app_env: str = os.getenv("APP_ENV", "development")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-before-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dae_erp.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    allow_origins: list[str] = Field(default_factory=lambda: os.getenv("ALLOW_ORIGINS", "*").split(","))
    allow_credentials: bool = False


settings = Settings()
