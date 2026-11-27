from pathlib import Path

import pytest
from pydantic import ValidationError

from app.config import load_document_settings


def test_load_document_settings(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        "size = 300\noverlap = 50\n",
        encoding="utf-8",
    )

    settings = load_document_settings(config_file)

    assert settings.size == 300
    assert settings.overlap == 50


def test_load_document_settings_invalid_overlap(tmp_path: Path):
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        "size = 100\noverlap = 150\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_document_settings(config_file)
