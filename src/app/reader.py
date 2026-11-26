from collections.abc import Iterator
from pathlib import Path


def read_documents(folder: Path) -> Iterator[tuple[Path, str]]:
    """
    Recursively read .md and .txt files from the given folder.

    Args:
        folder: Root directory containing documents.

    Yields:
        A tuple containing the file path and its text content.
    """
    for file_path in folder.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in {".md", ".txt"}:
            text = file_path.read_text(encoding="utf-8")
            yield file_path, text
