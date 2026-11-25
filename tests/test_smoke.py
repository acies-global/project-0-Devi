from app.config import Settings
from app.main import main


def test_settings_read_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("APP_ENV", "test")
    settings = Settings(_env_file=None)
    assert settings.app_env == "test"
    assert settings.api_key.get_secret_value() == "test-key"


def test_main_runs(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    main()
