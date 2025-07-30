# Do not import anything else from artha here

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_prefix="ARTHA_",
        env_file_encoding="utf-8",
    )


settings = Settings()
