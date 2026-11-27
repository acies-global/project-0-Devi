from collections.abc import Iterator
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


def read_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    return "\n\n".join(pages)


def read_documents(folder: Path) -> Iterator[tuple[Path, str]]:
    """
    Recursively read .md, .txt and .pdf files from the given folder.

    Args:
        folder: Root directory containing documents.

    Yields:
        A tuple containing the file path and its text content.
    """

    for file_path in folder.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        if file_path.suffix.lower() == ".pdf":
            text = read_pdf(file_path)
        else:
            text = file_path.read_text(encoding="utf-8")

        yield file_path, text
