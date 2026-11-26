
import argparse
from pathlib import Path

from pydantic import ValidationError

from app.models import Settings
from app.pipeline import build_chunks
from app.writer import write_chunks


def main() -> None:
    """Run the document toolkit CLI."""

    parser = argparse.ArgumentParser(
        description="Read, clean and chunk documents into JSON."
    )

    parser.add_argument(
        "folder",
        type=Path,
        help="Input folder containing documents",
    )

    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output JSON file path",
    )

    parser.add_argument(
        "--size",
        type=int,
        default=200,
        help="Number of words per chunk (default: 200)",
    )

    parser.add_argument(
        "--overlap",
        type=int,
        default=40,
        help="Number of overlapping words (default: 40)",
    )

    args = parser.parse_args()

    # Validate input folder
    if not args.folder.is_dir():
        parser.error(f"Input folder does not exist: {args.folder}")

    # Validate settings
    try:
        settings = Settings(
            size=args.size,
            overlap=args.overlap,
        )
    except ValidationError as exc:
        parser.error(str(exc))

    # Build chunks
    chunks = build_chunks(args.folder, settings)

    # Write JSON output
    write_chunks(chunks, args.out)

    # Count documents represented in the generated chunks
    document_count = len({chunk.source for chunk in chunks})

    print(
        f"Wrote {len(chunks)} chunks from "
        f"{document_count} non-empty documents to {args.out}"
    )
