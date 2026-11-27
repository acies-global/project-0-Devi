from app import reader


def test_read_pdf_extracts_text(tmp_path, monkeypatch):
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.touch()

    class FakePage:
        def extract_text(self):
            return "Hello PDF"

    class FakePdfReader:
        def __init__(self, file_path):
            self.pages = [FakePage(), FakePage()]

    monkeypatch.setattr(reader, "PdfReader", FakePdfReader)

    result = reader.read_pdf(pdf_file)

    assert result == "Hello PDF\n\nHello PDF"


def test_read_documents_supports_pdf(tmp_path, monkeypatch):
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.touch()

    monkeypatch.setattr(
        reader,
        "read_pdf",
        lambda file_path: "Extracted PDF content",
    )

    documents = list(reader.read_documents(tmp_path))

    assert len(documents) == 1
    assert documents[0][0] == pdf_file
    assert documents[0][1] == "Extracted PDF content"


def test_read_documents_supports_txt_and_md(tmp_path):
    (tmp_path / "sample.txt").write_text(
        "Text content",
        encoding="utf-8",
    )
    (tmp_path / "sample.md").write_text(
        "Markdown content",
        encoding="utf-8",
    )

    documents = list(reader.read_documents(tmp_path))

    assert len(documents) == 2
    assert {path.suffix for path, _ in documents} == {".txt", ".md"}
