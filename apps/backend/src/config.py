"""Application configuration — Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Sentinel Life OS backend configuration."""

    # Application
    app_name: str = "Sentinel Life OS API"
    app_version: str = "0.1.0"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./data/sentinel_auth.db"

    # JWT
    jwt_secret: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = [
        "http://localhost:4200",
        "http://localhost:3000",
        "https://sentinel-life-os.vercel.app",
    ]

    # Rate limiting
    rate_limit_auth: str = "10/minute"
    rate_limit_general: str = "100/minute"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
