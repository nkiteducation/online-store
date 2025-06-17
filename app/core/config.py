from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseModel):
    model_config = ConfigDict(frozen=True)


class APISettings(Settings):
    host: str = "127.0.0.1"
    port: int = 8080
    workers: int = 1


class URLSettings(Settings):
    drivername: str = "postgresql+asyncpg"
    username: str = "postgres"
    password: str = "password"
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"

    def get(self) -> URL:
        return URL.create(
            drivername=self.drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


class DBSettings(Settings):
    poolSize: int = 5
    maxOverflow: int = 10
    poolTimeout: int = 30

    url: URLSettings = URLSettings()


class AuthJWTSettings(BaseSettings):
    private_key_path: Path = next(
        Path().rglob("private.pem"),
        FileNotFoundError("private.pem"),
    )
    public_key_path: Path = next(
        Path().rglob("public.pem"),
        FileNotFoundError("public.pem"),
    )

    access_token_lifetime: timedelta = timedelta(minutes=15)
    refresh_token_lifetime: timedelta = timedelta(days=30)


class AppSettings(BaseSettings):
    development: bool = False

    api: APISettings = APISettings()
    database: DBSettings = DBSettings()
    jwt: AuthJWTSettings = AuthJWTSettings()

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
        env_ignore_empty=True,
    )


settings = AppSettings()
