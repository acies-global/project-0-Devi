from pathlib import Path

from app.chunker import chunk_words
from app.cleaner import clean_text
from app.models import Chunk, Settings
from app.reader import read_documents


def build_chunks(folder: Path, settings: Settings) -> list[Chunk]:
    """Read, clean and chunk every supported document."""
    chunks: list[Chunk] = []

    for file_path, original_text in read_documents(folder):
        cleaned_text = clean_text(original_text)

        text_chunks = chunk_words(
            cleaned_text,
            size=settings.size,
            overlap=settings.overlap,
        )

        source = file_path.relative_to(folder).as_posix()

        for position, chunk_text in enumerate(text_chunks):
            chunk = Chunk(
                id=f"{source}#{position}",
                source=source,
                position=position,
                text=chunk_text,
                word_count=len(chunk_text.split()),
            )
            chunks.append(chunk)

    return chunks
