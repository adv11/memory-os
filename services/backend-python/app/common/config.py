import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_env_file = os.environ.get("ENV_FILE", ".env")


class Settings(BaseSettings):
    database_url: str
    google_client_id: str
    google_client_secret: str
    secret_key: str
    cors_allowed_origins: list[str] = ["http://localhost:3000"]
    web_success_url: str = "http://localhost:3000/dashboard"
    web_logout_success_url: str = "http://localhost:3000"
    cookie_secure: bool = False
    port: int = 8080

    model_config = SettingsConfigDict(env_file=_env_file, extra="ignore")


settings = Settings()
