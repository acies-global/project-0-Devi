from collections import Counter

from app.models import Chunk


def build_summary_report(
    chunks: list[Chunk],
    chunk_size: int,
) -> dict:
    """Calculate document and chunk statistics."""

    document_count = len({chunk.source for chunk in chunks})
    total_words = sum(chunk.word_count for chunk in chunks)
    total_chunks = len(chunks)

    average_chunk_size = round(total_words / total_chunks, 2) if total_chunks else 0

    # Divide the configured chunk size into four ranges.
    bucket_width = max(1, chunk_size // 4)
    distribution = Counter()

    for chunk in chunks:
        words = chunk.word_count

        if words > bucket_width * 4:
            label = f">{bucket_width * 4}"
        else:
            bucket = (words - 1) // bucket_width
            lower = bucket * bucket_width + 1
            upper = (bucket + 1) * bucket_width
            label = f"{lower}-{upper}"

        distribution[label] += 1

    return {
        "document_count": document_count,
        "total_words": total_words,
        "total_chunks": total_chunks,
        "average_chunk_size": average_chunk_size,
        "chunk_size_distribution": dict(
            sorted(
                distribution.items(),
                key=lambda item: (
                    int(item[0].split("-")[0])
                    if item[0].startswith(tuple("0123456789"))
                    else float("inf")
                ),
            )
        ),
    }


def format_summary_report(report: dict) -> str:
    """Format statistics as a readable report."""

    lines = [
        "Document Toolkit Summary",
        "------------------------",
        f"Documents processed: {report['document_count']}",
        f"Total words: {report['total_words']}",
        f"Total chunks: {report['total_chunks']}",
        f"Average chunk size: {report['average_chunk_size']} words",
        "",
        "Chunk size distribution:",
    ]

    for size_range, count in report["chunk_size_distribution"].items():
        lines.append(f"{size_range} words: {count} chunks")

    return "\n".join(lines)
