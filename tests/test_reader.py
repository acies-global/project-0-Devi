from pathlib import Path

from app.reader import read_documents


def test_reads_only_text_files(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("world", encoding="utf-8")
    (tmp_path / "c.png").write_bytes(b"\x89PNG")

    names = sorted(path.name for path, _ in read_documents(tmp_path))

    assert names == ["a.md", "b.txt"]
