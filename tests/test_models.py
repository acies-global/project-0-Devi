import pytest
from pydantic import ValidationError

from app.models import Chunk, Settings


def test_chunk_model() -> None:
    chunk = Chunk(
        id="tutorial/first-steps.md#0",
        source="tutorial/first-steps.md",
        position=0,
        text="Python is a programming",
        word_count=4,
    )

    assert chunk.id == "tutorial/first-steps.md#0"
    assert chunk.source == "tutorial/first-steps.md"
    assert chunk.position == 0
    assert chunk.word_count == 4


def test_chunk_model_dump_has_exact_fields() -> None:
    chunk = Chunk(
        id="tutorial/first-steps.md#0",
        source="tutorial/first-steps.md",
        position=0,
        text="Python is a programming",
        word_count=4,
    )

    assert set(chunk.model_dump().keys()) == {
        "id",
        "source",
        "position",
        "text",
        "word_count",
    }


def test_chunk_rejects_negative_position() -> None:
    with pytest.raises(ValidationError):
        Chunk(
            id="example.md#-1",
            source="example.md",
            position=-1,
            text="Hello world",
            word_count=2,
        )


def test_default_settings() -> None:
    settings = Settings()

    assert settings.size == 200
    assert settings.overlap == 40


def test_custom_settings() -> None:
    settings = Settings(size=100, overlap=20)

    assert settings.size == 100
    assert settings.overlap == 20


@pytest.mark.parametrize(
    ("size", "overlap"),
    [
        (100, 100),
        (100, 101),
        (0, 0),
        (-1, 0),
        (100, -1),
    ],
)
def test_invalid_settings(size: int, overlap: int) -> None:
    with pytest.raises(ValidationError):
        Settings(size=size, overlap=overlap)
