import re


def clean_text(text: str) -> str:
    """
    Clean document text by normalizing whitespace,
    removing include markers, and preserving paragraph breaks.
    """

    # Remove include markers
    text = re.sub(r"\{\*.*?\*\}", "", text)

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        cleaned_line = " ".join(line.split())

        if cleaned_line:
            cleaned_lines.append(cleaned_line)
        elif cleaned_lines and cleaned_lines[-1] != "":
            cleaned_lines.append("")

    return "\n".join(cleaned_lines).strip()
