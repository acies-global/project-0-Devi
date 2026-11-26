def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    """
    Split text into word-based chunks with configurable overlap.
    """

    if size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative.")

    if overlap >= size:
        raise ValueError("Overlap must be smaller than chunk size.")

    words = text.split()

    if not words:
        return []

    step = size - overlap
    chunks = []

    for start in range(0, len(words), step):
        chunk = words[start : start + size]

        chunks.append(" ".join(chunk))

        # Stop when the current chunk reaches the end of the text.
        if start + size >= len(words):
            break

    return chunks
