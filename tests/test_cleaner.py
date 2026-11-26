from app.cleaner import clean_text


def test_removes_extra_spaces() -> None:
    text = "Hello     World"
    assert clean_text(text) == "Hello World"


def test_preserves_paragraph_breaks() -> None:
    text = "Hello\n\n\n\nWorld"
    assert clean_text(text) == "Hello\n\nWorld"


def test_removes_trailing_whitespace() -> None:
    text = "Hello   \nWorld   "
    assert clean_text(text) == "Hello\nWorld"


def test_empty_text() -> None:
    assert clean_text("") == ""


def test_removes_include_markers() -> None:
    text = "Getting Started\n\n{* ../../docs_src/first_steps/tutorial001.py *}\n\nLearn Python"
    expected = "Getting Started\n\nLearn Python"

    assert clean_text(text) == expected


def test_removes_multiple_include_markers() -> None:
    text = (
        "Introduction\n\n"
        "{* ../../docs_src/example1.py *}\n\n"
        "Some explanation\n\n"
        "{* ../../docs_src/example2.py *}\n\n"
        "Conclusion"
    )
    expected = "Introduction\n\nSome explanation\n\nConclusion"

    assert clean_text(text) == expected


def test_include_marker_only() -> None:
    text = "{* ../../docs_src/example.py *}"
    assert clean_text(text) == ""
