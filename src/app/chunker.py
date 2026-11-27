import re


def _split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split Markdown text into heading and content sections."""

    sections: list[tuple[str, str]] = []
    current_heading = ""
    current_lines: list[str] = []

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if current_heading or current_lines:
                sections.append((current_heading, "\n".join(current_lines).strip()))

            current_heading = line.strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading or current_lines:
        sections.append((current_heading, "\n".join(current_lines).strip()))

    return sections


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using punctuation boundaries."""

    sentences: list[str] = []

    for paragraph in re.split(r"\n\s*\n", text.strip()):
        paragraph = " ".join(paragraph.split())

        if not paragraph:
            continue

        parts = re.split(r"(?<=[.!?])\s+", paragraph)

        sentences.extend(sentence.strip() for sentence in parts if sentence.strip())

    return sentences


def _chunk_sentences(
    sentences: list[str],
    size: int,
    overlap: int,
    heading: str = "",
) -> list[str]:
    """Create chunks without splitting individual sentences."""

    if not sentences:
        return [heading] if heading else []

    heading_words = len(heading.split())
    chunks: list[str] = []
    start = 0

    while start < len(sentences):
        current: list[str] = []
        word_count = heading_words
        end = start

        while end < len(sentences):
            sentence = sentences[end]
            sentence_words = len(sentence.split())

            if current and word_count + sentence_words > size:
                break

            # Keep a complete sentence even if it exceeds the limit.
            current.append(sentence)
            word_count += sentence_words
            end += 1

        chunk_text = " ".join(current)

        if heading:
            chunk_text = f"{heading}\n{chunk_text}".strip()

        chunks.append(chunk_text)

        if end >= len(sentences):
            break

        # Find complete sentences for the next chunk's overlap.
        next_start = end
        overlap_words = 0

        for index in range(end - 1, start - 1, -1):
            sentence_words = len(sentences[index].split())

            if overlap_words + sentence_words > overlap:
                break

            overlap_words += sentence_words
            next_start = index

        # Always make progress, even when a sentence is
        # larger than the requested overlap.
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def chunk_heading_sentence(
    text: str,
    size: int,
    overlap: int,
) -> list[str]:
    """
    Split text using heading-aware and sentence-aware chunking.

    Markdown headings are preserved with their content.
    Sentences are kept intact whenever possible.
    """

    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= size:
        raise ValueError("Overlap must be smaller than chunk size.")

    if not text.strip():
        return []

    sections = _split_into_sections(text)

    all_chunks: list[str] = []

    for heading, content in sections:
        sentences = _split_into_sentences(content)

        section_chunks = _chunk_sentences(
            sentences=sentences,
            size=size,
            overlap=overlap,
            heading=heading,
        )

        all_chunks.extend(section_chunks)

    return all_chunks


def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    """Split text into word-based chunks with configurable overlap."""

    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= size:
        raise ValueError("Overlap must be smaller than chunk size.")

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = end - overlap

    return chunks
