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

Generator-based document reading - Used a generator instead of returning all document contents at once. This reduces memory usage during reading because documents are yielded one at a time.

Whitespace cleaning instead of aggressive text normalization - Focused on removing unnecessary whitespace while preserving paragraph breaks. This keeps the original document structure more readable.

Removing include markers because their referenced code files are not available in the corpus. This avoids keeping incomplete references in the processed content.

Chose word-based chunking because it provides predictable chunk-size limits and straightforward control over overlap. Sentence-aware chunking could preserve sentence boundaries better, but it is outside the current implementation.

Configurable chunk size and overlap - Provided default values of 200 words and 40 overlapping words, while allowing users to override them through CLI arguments. This makes the application flexible for different document collections.

Used Pydantic to validate settings and define a consistent structure for generated chunks.

## Results

he Document Toolkit CLI provides an end-to-end workflow for processing a folder of text and Markdown documents.

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
```
