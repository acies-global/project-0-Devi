import pytest

from app.chunker import chunk_words


def test_normal_chunking_with_overlap() -> None:
    text = "a b c d e f"

    result = chunk_words(text, size=4, overlap=2)

    assert result == ["a b c d", "c d e f"]


def test_chunking_without_overlap() -> None:
    text = "a b c d e f"

    result = chunk_words(text, size=3, overlap=0)

    assert result == ["a b c", "d e f"]


def test_text_shorter_than_chunk_size() -> None:
    text = "a b"

    result = chunk_words(text, size=4, overlap=1)

    assert result == ["a b"]


def test_empty_text() -> None:
    assert chunk_words("", size=4, overlap=1) == []


def test_no_redundant_tail_chunk() -> None:
    text = "a b c d e f"

    result = chunk_words(text, size=4, overlap=2)

    assert result == ["a b c d", "c d e f"]


def test_whitespace_only_text() -> None:
    assert chunk_words("   \n  ", size=4, overlap=1) == []


@pytest.mark.parametrize(
    ("size", "overlap"),
    [
        (4, 4),
        (4, 5),
        (0, 0),
        (-1, 0),
        (4, -1),
    ],
)
def test_invalid_chunk_settings(size: int, overlap: int) -> None:
    with pytest.raises(ValueError):
        chunk_words("a b c d", size=size, overlap=overlap)
