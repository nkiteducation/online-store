from app.core.config import APISettings, AppSettings, settings


def test_default_settings():
    assert isinstance(settings, AppSettings)
    assert settings.development is False
    assert isinstance(settings.api, APISettings)
    assert settings.api.host == "127.0.0.1"
    assert settings.api.port == 8080
    assert settings.api.workers == 1


def test_env_override():
    env_settings = AppSettings()
    assert env_settings.development is True
    assert env_settings.api.host == "0.0.0.0"
    assert env_settings.api.port == 9090
    assert env_settings.api.workers == 4
