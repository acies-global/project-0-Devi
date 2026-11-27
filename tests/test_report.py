
from app.models import Chunk
from app.report import build_summary_report, format_summary_report


def make_chunk(source, position, text):
    return Chunk(
        id=f"{source}#{position}",
        source=source,
        position=position,
        text=text,
        word_count=len(text.split()),
    )


def test_report_counts_unique_documents():
    chunks = [
        make_chunk("a.txt", 0, "one two"),
        make_chunk("a.txt", 1, "three four"),
        make_chunk("b.txt", 0, "five six"),
    ]

    report = build_summary_report(chunks, 200)

    assert report["document_count"] == 2


def test_report_calculates_total_words():
    chunks = [
        make_chunk("a.txt", 0, "one two three"),
        make_chunk("b.txt", 0, "four five"),
    ]

    report = build_summary_report(chunks, 200)

    assert report["total_words"] == 5


def test_report_calculates_total_chunks():
    chunks = [
        make_chunk("a.txt", 0, "one two"),
        make_chunk("a.txt", 1, "three four"),
        make_chunk("b.txt", 0, "five"),
    ]

    report = build_summary_report(chunks, 200)

    assert report["total_chunks"] == 3


def test_report_calculates_average_chunk_size():
    chunks = [
        make_chunk("a.txt", 0, "one two three four"),
        make_chunk("b.txt", 0, "five six"),
    ]

    report = build_summary_report(chunks, 200)

    assert report["average_chunk_size"] == 3.0


def test_report_handles_empty_chunks():
    report = build_summary_report([], 200)

    assert report["document_count"] == 0
    assert report["total_words"] == 0
    assert report["total_chunks"] == 0
    assert report["average_chunk_size"] == 0


def test_report_distribution_first_bucket():
    chunks = [
        make_chunk("a.txt", 0, " ".join(["word"] * 25)),
    ]

    report = build_summary_report(chunks, 200)

    assert report["chunk_size_distribution"]["1-50"] == 1


def test_report_distribution_second_bucket():
    chunks = [
        make_chunk("a.txt", 0, " ".join(["word"] * 75)),
    ]

    report = build_summary_report(chunks, 200)

    assert report["chunk_size_distribution"]["51-100"] == 1


def test_report_distribution_third_bucket():
    chunks = [
        make_chunk("a.txt", 0, " ".join(["word"] * 125)),
    ]

    report = build_summary_report(chunks, 200)

    assert report["chunk_size_distribution"]["101-150"] == 1


def test_report_distribution_fourth_bucket():
    chunks = [
        make_chunk("a.txt", 0, " ".join(["word"] * 175)),
    ]

    report = build_summary_report(chunks, 200)

    assert report["chunk_size_distribution"]["151-200"] == 1


def test_report_distribution_above_chunk_size():
    chunks = [
        make_chunk("a.txt", 0, " ".join(["word"] * 201)),
    ]

    report = build_summary_report(chunks, 200)

    assert report["chunk_size_distribution"][">200"] == 1


def test_report_distribution_bucket_boundaries():
    sizes = [1, 50, 51, 100, 101, 150, 151, 200, 201]

    chunks = [
        make_chunk(f"doc{i}.txt", 0, " ".join(["word"] * size))
        for i, size in enumerate(sizes)
    ]

    report = build_summary_report(chunks, 200)

    distribution = report["chunk_size_distribution"]

    assert distribution["1-50"] == 2
    assert distribution["51-100"] == 2
    assert distribution["101-150"] == 2
    assert distribution["151-200"] == 2
    assert distribution[">200"] == 1


def test_report_formats_summary():
    chunks = [
        make_chunk("a.txt", 0, "one two three"),
        make_chunk("b.txt", 0, "four five"),
    ]

    report = build_summary_report(chunks, 200)
    formatted = format_summary_report(report)

    assert "Document Toolkit Summary" in formatted
    assert "Documents processed: 2" in formatted
    assert "Total words: 5" in formatted
    assert "Total chunks: 2" in formatted
    assert "Average chunk size:" in formatted
    assert "Chunk size distribution:" in formatted
