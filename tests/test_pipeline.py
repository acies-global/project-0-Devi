
from app.models import Settings
from app.pipeline import build_chunks


def test_pipeline_processes_multiple_files(tmp_path):
    (tmp_path / "first.txt").write_text(
        "This is the first document.",
        encoding="utf-8",
    )
    (tmp_path / "second.txt").write_text(
        "This is the second document.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    sources = {chunk.source for chunk in chunks}

    assert "first.txt" in sources
    assert "second.txt" in sources


def test_pipeline_processes_nested_folders(tmp_path):
    nested = tmp_path / "folder" / "nested"
    nested.mkdir(parents=True)

    (nested / "sample.txt").write_text(
        "This is a nested document.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    assert len(chunks) > 0
    assert chunks[0].source == "folder/nested/sample.txt"


def test_pipeline_returns_empty_for_empty_folder(tmp_path):
    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    assert chunks == []


def test_pipeline_skips_empty_documents(tmp_path):
    (tmp_path / "empty.txt").write_text("", encoding="utf-8")
    (tmp_path / "valid.txt").write_text(
        "This is a valid document.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    assert chunks
    assert all(chunk.source == "valid.txt" for chunk in chunks)


def test_pipeline_skips_whitespace_documents(tmp_path):
    (tmp_path / "spaces.txt").write_text(
        "   \n   \t   ",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    assert chunks == []



def test_pipeline_generates_unique_chunk_ids(tmp_path):
    (tmp_path / "sample.txt").write_text(
        "This is a sample sentence. " * 500,
        encoding="utf-8",
    )

    chunks = build_chunks(
        tmp_path,
        Settings(size=100, overlap=20),
    )

    ids = [chunk.id for chunk in chunks]

    assert len(ids) > 1
    assert len(ids) == len(set(ids))



def test_pipeline_generates_correct_chunk_positions(tmp_path):
    (tmp_path / "sample.txt").write_text(
        " ".join(["word"] * 500),
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=100, overlap=20))

    positions = [
        chunk.position
        for chunk in chunks
    ]

    assert positions == list(range(len(chunks)))


def test_pipeline_generates_ids_from_source_and_position(tmp_path):
    (tmp_path / "sample.txt").write_text(
        "This is a sample document.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    for chunk in chunks:
        assert chunk.id == f"{chunk.source}#{chunk.position}"


def test_pipeline_calculates_word_count(tmp_path):
    (tmp_path / "sample.txt").write_text(
        "One two three four five.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    assert chunks[0].word_count == len(chunks[0].text.split())


def test_pipeline_preserves_document_order(tmp_path):
    (tmp_path / "first.txt").write_text(
        "First document.",
        encoding="utf-8",
    )
    (tmp_path / "second.txt").write_text(
        "Second document.",
        encoding="utf-8",
    )

    chunks = build_chunks(tmp_path, Settings(size=200, overlap=40))

    sources = [chunk.source for chunk in chunks]

    assert sources.index("first.txt") < sources.index("second.txt")
