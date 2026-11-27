import sys
from unittest.mock import patch

import pytest

from app import cli
from app.models import Chunk


def make_chunk():
    return Chunk(
        id="sample.txt#0",
        source="sample.txt",
        position=0,
        text="This is a sample document.",
        word_count=5,
    )


def test_cli_runs_successfully(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    output_file = tmp_path / "chunks.json"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(output_file),
        ],
    )

    with (
        patch("app.cli.build_chunks", return_value=[make_chunk()]) as build,
        patch("app.cli.write_chunks") as writer,
    ):
        cli.main()

    build.assert_called_once()
    writer.assert_called_once()


def test_cli_rejects_missing_input_folder(tmp_path, monkeypatch):
    missing_folder = tmp_path / "missing"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(missing_folder),
            "--out",
            str(tmp_path / "chunks.json"),
        ],
    )

    with pytest.raises(SystemExit):
        cli.main()


def test_cli_requires_output_argument(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        ["app", str(input_folder)],
    )

    with pytest.raises(SystemExit):
        cli.main()


def test_cli_uses_default_chunk_settings(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
        ],
    )

    with patch("app.cli.build_chunks", return_value=[]) as build, patch("app.cli.write_chunks"):
        cli.main()

    settings = build.call_args.args[1]

    assert settings.size == 200
    assert settings.overlap == 40


def test_cli_accepts_custom_chunk_size(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--size",
            "100",
        ],
    )

    with patch("app.cli.build_chunks", return_value=[]) as build, patch("app.cli.write_chunks"):
        cli.main()

    settings = build.call_args.args[1]

    assert settings.size == 100


def test_cli_accepts_custom_overlap(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--overlap",
            "20",
        ],
    )

    with patch("app.cli.build_chunks", return_value=[]) as build, patch("app.cli.write_chunks"):
        cli.main()

    settings = build.call_args.args[1]

    assert settings.overlap == 20


def test_cli_rejects_invalid_chunk_size(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--size",
            "0",
        ],
    )

    with pytest.raises(SystemExit):
        cli.main()


def test_cli_rejects_invalid_overlap(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--size",
            "100",
            "--overlap",
            "100",
        ],
    )

    with pytest.raises(SystemExit):
        cli.main()


def test_cli_calls_writer_with_generated_chunks(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    output_file = tmp_path / "chunks.json"
    chunks = [make_chunk()]

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(output_file),
        ],
    )

    with (
        patch("app.cli.build_chunks", return_value=chunks),
        patch("app.cli.write_chunks") as writer,
    ):
        cli.main()

    writer.assert_called_once_with(chunks, output_file)


def test_cli_accepts_custom_toml_config(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    config_file = tmp_path / "settings.toml"
    config_file.write_text(
        "size = 150\noverlap = 30\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--config",
            str(config_file),
        ],
    )

    with patch("app.cli.build_chunks", return_value=[]) as build, patch("app.cli.write_chunks"):
        cli.main()

    settings = build.call_args.args[1]

    assert settings.size == 150
    assert settings.overlap == 30


def test_cli_arguments_override_toml_config(tmp_path, monkeypatch):
    input_folder = tmp_path / "documents"
    input_folder.mkdir()

    config_file = tmp_path / "settings.toml"
    config_file.write_text(
        "size = 150\noverlap = 30\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "app",
            str(input_folder),
            "--out",
            str(tmp_path / "chunks.json"),
            "--config",
            str(config_file),
            "--size",
            "100",
            "--overlap",
            "20",
        ],
    )

    with patch("app.cli.build_chunks", return_value=[]) as build, patch("app.cli.write_chunks"):
        cli.main()

    settings = build.call_args.args[1]

    assert settings.size == 100
    assert settings.overlap == 20
