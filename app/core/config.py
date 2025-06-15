from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True)


class APISettings(Settings):
    host: str = "127.0.0.1"
    port: int = 8080
    workers: int = 1


class AppSettings(BaseSettings):
    development: bool = False

    api: APISettings = APISettings()

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        env_ignore_empty=True,
    )


settings = AppSettings()
