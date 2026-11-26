
import json
from pathlib import Path

from app.models import Chunk


def write_chunks(chunks: list[Chunk], output_path: Path) -> None:
    """Save all chunks to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [chunk.model_dump() for chunk in chunks]

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
