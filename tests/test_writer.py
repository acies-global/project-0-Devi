
import json

from app.models import Chunk
from app.writer import write_chunks


def make_chunk():
    return Chunk(
        id="docs/sample.txt#0",
        source="docs/sample.txt",
        position=0,
        text="This is a sample document.",
        word_count=5,
    )


def test_write_chunks_creates_json_file(tmp_path):
    output = tmp_path / "chunks.json"

    write_chunks([make_chunk()], output)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))
    assert len(data) == 1


def test_write_chunks_creates_parent_directory(tmp_path):
    output = tmp_path / "nested" / "folder" / "chunks.json"

    write_chunks([make_chunk()], output)

    assert output.exists()
    assert output.parent.is_dir()


def test_write_empty_chunks(tmp_path):
    output = tmp_path / "chunks.json"

    write_chunks([], output)

    assert json.loads(output.read_text(encoding="utf-8")) == []


def test_write_chunks_contains_all_model_fields(tmp_path):
    output = tmp_path / "chunks.json"

    chunk = make_chunk()
    write_chunks([chunk], output)

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data[0] == chunk.model_dump()


def test_write_chunks_preserves_unicode(tmp_path):
    output = tmp_path / "chunks.json"

    chunk = Chunk(
        id="sample.txt#0",
        source="sample.txt",
        position=0,
        text="Hello नमस्ते café",
        word_count=3,
    )

    write_chunks([chunk], output)

    content = output.read_text(encoding="utf-8")
    assert "नमस्ते" in content
    assert "café" in content


def test_write_chunks_overwrites_existing_file(tmp_path):
    output = tmp_path / "chunks.json"
    output.write_text('{"old": "data"}', encoding="utf-8")

    write_chunks([make_chunk()], output)

    data = json.loads(output.read_text(encoding="utf-8"))

    assert isinstance(data, list)
    assert data[0]["id"] == "docs/sample.txt#0"
