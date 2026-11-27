import argparse
import logging
import tomllib
from pathlib import Path

from pydantic import ValidationError

from app.config import load_document_settings
from app.models import Settings
from app.pipeline import build_chunks
from app.writer import write_chunks

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the document toolkit CLI."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="Read, clean and chunk documents into JSON.")

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
        "--config",
        type=Path,
        default=Path("config.toml"),
        help="Path to TOML configuration file",
    )

    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help="Number of words per chunk (overrides TOML)",
    )

    parser.add_argument(
        "--overlap",
        type=int,
        default=None,
        help="Number of overlapping words (overrides TOML)",
    )

    args = parser.parse_args()

    # Validate input folder
    if not args.folder.is_dir():
        parser.error(f"Input folder does not exist: {args.folder}")

    # Load and validate document settings
    try:
        document_settings = load_document_settings(args.config)

        settings_data = document_settings.model_dump()

        # CLI arguments override TOML values
        if args.size is not None:
            settings_data["size"] = args.size

        if args.overlap is not None:
            settings_data["overlap"] = args.overlap

        settings = Settings.model_validate(settings_data)

    except (ValidationError, OSError, tomllib.TOMLDecodeError) as exc:
        parser.error(f"Invalid configuration: {exc}")

    logger.info(
        "Using document settings: size=%d, overlap=%d",
        settings.size,
        settings.overlap,
    )

    # Build chunks
    chunks = build_chunks(args.folder, settings)

    # Write JSON output
    write_chunks(chunks, args.out)

    # Count documents represented in the generated chunks
    document_count = len({chunk.source for chunk in chunks})

    logger.info(
        "Wrote %d chunks from %d non-empty documents to %s",
        len(chunks),
        document_count,
        args.out,
    )


if __name__ == "__main__":
    main()
