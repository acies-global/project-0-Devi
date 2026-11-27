import pytest

from app.chunker import chunk_heading_sentence, chunk_words


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


def test_whitespace_only_text() -> None:
    assert chunk_words("   \n  ", size=4, overlap=1) == []


def test_no_redundant_tail_chunk() -> None:
    text = "a b c d e f"

    result = chunk_words(text, size=4, overlap=2)

    assert result == ["a b c d", "c d e f"]


def test_exact_chunk_size() -> None:
    text = "a b c d"

    result = chunk_words(text, size=4, overlap=0)

    assert result == ["a b c d"]


def test_multiple_chunks_with_overlap() -> None:
    text = "one two three four five six seven eight nine"

    result = chunk_words(text, size=4, overlap=1)

    assert result == [
        "one two three four",
        "four five six seven",
        "seven eight nine",
    ]


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
def test_invalid_word_chunk_settings(
    size: int,
    overlap: int,
) -> None:
    with pytest.raises(ValueError):
        chunk_words("a b c d", size=size, overlap=overlap)


def test_heading_aware_chunking() -> None:
    text = """# Authentication

Authentication verifies user identity.

# Authorization

Authorization determines user permissions."""

    chunks = chunk_heading_sentence(text, size=200, overlap=40)

    assert len(chunks) == 2
    assert chunks[0].startswith("# Authentication")
    assert chunks[1].startswith("# Authorization")


def test_multiple_markdown_heading_levels() -> None:
    text = """# Main Heading

Main content.

## Sub Heading

Subheading content.

### Third Level Heading

Third-level content."""

    chunks = chunk_heading_sentence(text, size=200, overlap=0)

    assert len(chunks) == 3
    assert chunks[0].startswith("# Main Heading")
    assert chunks[1].startswith("## Sub Heading")
    assert chunks[2].startswith("### Third Level Heading")


def test_text_before_first_heading() -> None:
    text = """Introduction paragraph.

# Main Heading

Main heading content."""

    chunks = chunk_heading_sentence(text, size=200, overlap=0)

    assert len(chunks) == 2
    assert chunks[0] == "Introduction paragraph."
    assert chunks[1].startswith("# Main Heading")


def test_heading_is_preserved_in_multiple_chunks() -> None:
    text = """# Authentication

First sentence has several words here.
Second sentence has several words here.
Third sentence has several words here."""

    chunks = chunk_heading_sentence(text, size=9, overlap=0)

    assert len(chunks) > 1

    assert all(chunk.startswith("# Authentication") for chunk in chunks)


def test_heading_only_document() -> None:
    text = "# Authentication"

    chunks = chunk_heading_sentence(text, size=100, overlap=0)

    assert chunks == ["# Authentication"]


def test_multiple_headings_without_content() -> None:
    text = """# Authentication

## Authorization

### Security"""

    chunks = chunk_heading_sentence(text, size=100, overlap=0)

    assert chunks == [
        "# Authentication",
        "## Authorization",
        "### Security",
    ]


def test_document_without_headings() -> None:
    text = """First paragraph has some content.

Second paragraph has more content."""

    chunks = chunk_heading_sentence(text, size=100, overlap=0)

    assert len(chunks) == 1
    assert "First paragraph" in chunks[0]
    assert "Second paragraph" in chunks[0]


def test_sentence_aware_chunking() -> None:
    text = (
        "First sentence is complete. Second sentence is also complete. Third sentence is complete."
    )

    chunks = chunk_heading_sentence(text, size=7, overlap=0)

    assert len(chunks) > 1

    assert all(chunk.endswith(".") for chunk in chunks)


def test_sentences_are_not_split_between_chunks() -> None:
    text = (
        "The user enters their username. "
        "The system validates the username. "
        "The system grants access."
    )

    chunks = chunk_heading_sentence(text, size=6, overlap=0)

    expected_sentences = [
        "The user enters their username.",
        "The system validates the username.",
        "The system grants access.",
    ]

    for sentence in expected_sentences:
        assert sum(sentence in chunk for chunk in chunks) == 1


def test_multiple_paragraphs() -> None:
    text = """First paragraph contains a sentence.

Second paragraph contains another sentence.

Third paragraph contains a final sentence."""

    chunks = chunk_heading_sentence(text, size=100, overlap=0)

    assert len(chunks) == 1
    assert "First paragraph" in chunks[0]
    assert "Second paragraph" in chunks[0]
    assert "Third paragraph" in chunks[0]


def test_exclamation_and_question_mark_boundaries() -> None:
    text = "Are you authenticated? Access granted! The session is active."

    chunks = chunk_heading_sentence(text, size=5, overlap=0)

    assert len(chunks) > 1


def test_sentence_overlap() -> None:
    text = (
        "First sentence has four words. "
        "Second sentence has four words. "
        "Third sentence has four words."
    )

    chunks = chunk_heading_sentence(text, size=10, overlap=5)

    assert len(chunks) == 2

    assert chunks == [
        ("First sentence has four words. Second sentence has four words."),
        ("Second sentence has four words. Third sentence has four words."),
    ]


def test_zero_overlap() -> None:
    text = "First sentence has four words. Second sentence has four words."

    chunks = chunk_heading_sentence(text, size=4, overlap=0)

    assert len(chunks) == 2

    assert "First sentence has four words." in chunks[0]
    assert "Second sentence has four words." in chunks[1]


def test_long_sentence_is_preserved() -> None:
    text = "This is a very long sentence containing more words than the configured chunk size."

    chunks = chunk_heading_sentence(text, size=4, overlap=0)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_empty_heading_chunking() -> None:
    assert chunk_heading_sentence("", size=200, overlap=40) == []


def test_whitespace_only_heading_chunking() -> None:
    assert (
        chunk_heading_sentence(
            "   \n  \n   ",
            size=100,
            overlap=0,
        )
        == []
    )


@pytest.mark.parametrize(
    ("size", "overlap"),
    [
        (0, 0),
        (-1, 0),
        (10, 10),
        (10, 11),
        (10, -1),
    ],
)
def test_invalid_heading_chunk_settings(
    size: int,
    overlap: int,
) -> None:
    with pytest.raises(ValueError):
        chunk_heading_sentence(
            "Some text.",
            size=size,
            overlap=overlap,
        )
