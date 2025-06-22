from app.core.config import (
    APISettings,
    AppSettings,
    DBSettings,
    URLSettings,
    settings,
)


def test_default_settings() -> None:
    assert isinstance(settings, AppSettings)
    assert settings.development is False
    assert isinstance(settings.api, APISettings)
    assert settings.api.host == "127.0.0.1"
    assert settings.api.port == 8080
    assert settings.api.workers == 1

    assert isinstance(settings.database, DBSettings)
    assert settings.database.poolSize == 5
    assert settings.database.maxOverflow == 10
    assert settings.database.poolTimeout == 30

    assert isinstance(settings.database.url, URLSettings)
    assert settings.database.url.drivername == "postgresql+asyncpg"
    assert settings.database.url.username == "postgres"
    assert settings.database.url.password == "password"
    assert settings.database.url.host == "localhost"
    assert settings.database.url.port == 5432
    assert settings.database.url.database == "postgres"

    url_obj = settings.database.url.get()
    assert url_obj.render_as_string(hide_password=False).startswith(
        "postgresql+asyncpg://postgres:password@localhost:5432/postgres",
    )


def test_url_get_method() -> None:
    url_settings = URLSettings()
    url = url_settings.get()
    assert url.drivername == "postgresql+asyncpg"
    assert url.username == "postgres"
    assert url.password == "password"
    assert url.host == "localhost"
    assert url.port == 5432
    assert url.database == "postgres"


def test_db_settings_defaults() -> None:
    db_settings = DBSettings()
    assert db_settings.poolSize == 5
    assert db_settings.maxOverflow == 10
    assert db_settings.poolTimeout == 30
    assert isinstance(db_settings.url, URLSettings)


def test_api_settings_defaults() -> None:
    api_settings = APISettings()
    assert api_settings.host == "127.0.0.1"
    assert api_settings.port == 8080
    assert api_settings.workers == 1
