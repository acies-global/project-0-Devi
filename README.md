# gai-project-template 

Document Toolkit CLI

## Problem

Processing a collection of text documents manually can be time-consuming, especially when documents are stored across multiple folders and contain inconsistent whitespace or formatting.

The Document Toolkit CLI solves this problem by providing a simple command-line application that reads, cleans, and splits documents into smaller text chunks.

It is designed for developers and anyone who needs to prepare a collection of text documents for further processing, analysis, or downstream applications.

The application supports .txt and .md files, including files inside nested subdirectories. It generates a single JSON file containing all the processed chunks, along with their source file paths and positions.

Features

Recursively reads .txt and .md files.
Uses a generator to read documents one at a time.
Cleans unnecessary whitespace while preserving paragraph breaks.
Removes include markers that reference external code files not available in the corpus.
Splits documents into word-based chunks with configurable size and overlap.
Generates chunk IDs, source paths, positions, and word counts.
Validates chunking settings using Pydantic.
Saves all generated chunks into a single JSON file.
Provides a command-line interface (CLI).

## Design

The application is divided into small modules, with each module responsible for one part of the document-processing workflow.

The application processes documents through the following stages:

# Read documents (reader.py)

Uses Python's pathlib to recursively find .txt and .md files inside the input folder.
The read_documents() function is implemented as a generator that yields one (path, text) pair at a time. This avoids loading every source document into memory at once.

# Clean text (cleaner.py)

Cleans the document content before chunking. The cleaning operations include:
Collapsing repeated spaces, Removing leading and trailing whitespace, Removing trailing whitespace from lines,Normalizing unnecessary blank lines while preserving paragraph breaks, Removing include markers such as {* ../../docs_src/first_steps/tutorial001.py *}.Include markers are removed because they refer to external code files that are not available in the corpus. Keeping these markers would leave references to unavailable content in the processed text. Removing them keeps the generated chunks cleaner and avoids carrying incomplete references into the output.

# Chunk text (chunker.py)

Splits cleaned text into word-based chunks.
Each chunk contains a maximum of 200 words. The next chunk starts size - overlap words after the previous chunk's starting position.
For example, with a chunk size of 10 words and an overlap of 3 words:
Chunk 1: Words 1–10
Chunk 2: Words 8–17
Chunk 3: Words 15–24
Overlapping words help preserve context between consecutive chunks.

# Model the output (models.py)
Uses Pydantic to define two models Chunk and Settings
Invalid settings are rejected. For example, chunk size must be greater than zero, overlap cannot be negative, and overlap must be smaller than chunk size.

# Integrate the workflow (pipeline.py)

Combines the reader, cleaner, and chunker. It processes each document, creates Chunk objects, and assigns the required metadata.

Each chunk contains:
    id: Unique chunk identifier.
    source: Relative path of the original document.
    position: Zero-based position of the chunk within its source document.
    text: Cleaned chunk content.
    word_count: Number of words in the chunk.


# Write JSON (writer.py)

Saves all generated chunks into one JSON file.
Each Pydantic model is converted into a dictionary using model_dump() before being serialized into JSON. This ensures the output follows the defined Chunk model schema.

# Command-line interface (cli.py, __main__.py)

Uses Python's argparse module to accept the input folder, output file, chunk size, and overlap from the command line. The CLI executes the complete processing pipeline and prints a one-line summary after successful execution.

# Word-based chunking

The chunk_words() function splits cleaned text into chunks based on a configurable word count.

Features:

Supports configurable chunk size (default: 200 words).
Supports configurable overlap between consecutive chunks.
Prevents unnecessary empty or redundant chunks.
Validates chunk size and overlap settings.
Returns an empty list when the input contains no words.

For example, with a chunk size of 10 words and an overlap of 3 words:

Chunk 1: Words 1–10
Chunk 2: Words 8–17
Chunk 3: Words 15–24
Overlapping words help preserve context between consecutive chunks.

# Heading-aware and sentence-aware chunking

The chunk_heading_sentence() function provides an additional strategy that considers Markdown headings, paragraphs, and sentence boundaries when creating chunks.

Features:

Identifies Markdown headings from level 1 to level 6.
Separates document content into sections based on headings.
Preserves headings in the generated chunks.
Splits paragraphs into sentences using punctuation boundaries such as periods, question marks, and exclamation marks.
Keeps complete sentences together whenever possible.
Supports configurable chunk size and sentence-based overlap.
Preserves complete sentences when calculating overlap between consecutive chunks.
Validates chunk size and overlap settings.

The heading-aware strategy attempts to keep related content together rather than splitting text at arbitrary word positions.

Note: Because complete sentences are preserved, a chunk may exceed the configured word limit if an individual sentence or its heading is larger than the limit. Sentence overlap is also approximate because only complete sentences are reused.

This implementation uses Python's regular expressions and standard string operations. It does not require an external AI model or LangChain.
JSON Output Format

The output is a JSON array containing all generated chunks.

Example:

[
  {
    "id": "python/intro.md#0",
    "source": "python/intro.md",
    "position": 0,
    "text": "Python is a programming language used for many applications.",
    "word_count": 9
  },
  {
    "id": "python/intro.md#1",
    "source": "python/intro.md",
    "position": 1,
    "text": "used for many applications, including automation and data analysis.",
    "word_count": 9
  }
]


## Trade-offs

- **Generator-based reading:** Used a generator instead of loading all documents into memory at once. This reduces memory usage during document reading by yielding one document at a time.

- **Whitespace cleaning:** Focused on removing unnecessary whitespace while preserving paragraph breaks instead of aggressively normalizing the content. This helps retain the original document structure.

- **Include marker removal:** Removed include markers because they reference external code files that are not available in the corpus. Processing these references would leave incomplete content in the generated chunks.

- **Chunk size and overlap:** Chose a default chunk size of 200 words and an overlap of 40 words. This provides manageable chunks while retaining some context between consecutive chunks. Both values can be configured through the CLI.

- **Multiple chunking strategies:** Implemented word-based chunking for predictable chunk sizes and heading-aware, sentence-aware chunking for better structural preservation. The latter prioritizes complete sentences, even when this means exceeding the configured chunk size.

- **Pydantic models:** Used Pydantic to validate configuration settings and maintain a consistent schema for generated chunks.

## Results

The Document Toolkit CLI provides an end-to-end workflow for processing a folder of text and Markdown documents.

The expected results include:

Reading supported documents recursively, including nested folders.
Cleaning document text while preserving paragraph breaks.
Splitting documents into configurable word-based chunks.
Generating chunk IDs and source metadata.
Exporting all chunks into one structured JSON file.
Providing a command-line interface for running the complete workflow.

Testing

The project includes tests for the main application components:
Reader: supported file types and recursive document discovery.
Cleaner: whitespace cleaning, paragraph preservation, and include-marker removal.
Chunker: chunk size and overlap behavior
Models: Pydantic validation and invalid settings.

## How to run

```bash
cp .env.example .env      # fill in real values
uv sync                   # install dependencies
uv run python -m app.main # run the app
uv run ruff check .       # lint
uv run ruff format --check .
uv run pytest             # tests
uv run python -m app <input folder > --out <output>  # run the cli
uv run python -m app corpus --out chunks.json # here corpus is the input folder and chunks.json is the output file
uv run pytest # run testcase 
uv run pytest --cov=app #for testing the testcase coverage
```

## Known Limitations

- The sentence-aware chunker uses regular expressions, so abbreviations, decimal numbers, and complex punctuation may cause incorrect sentence boundaries.
- Heading detection supports standard Markdown ATX headings but does not support every Markdown heading syntax.
- Markdown headings inside fenced code blocks may be incorrectly identified as document headings.
- Very long sentences or headings may produce chunks larger than the configured chunk size.
- Word counts are based on whitespace-separated words and may differ from language-model token counts.
- Word-based chunking does not preserve sentence or paragraph boundaries.
- Heading-aware and sentence-aware chunking is rule-based and does not understand the semantic meaning of document content.
- The application does not currently provide semantic chunking or AI-based content understanding.
- Only the document formats supported by the reader are processed; unsupported formats are ignored.