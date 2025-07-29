# Book Strands

A powerful CLI tool for managing e-book metadata and organizing your digital library.

## Overview

Book Strands is designed to help you manage your e-book collection by providing tools to read, modify, and organize e-book metadata. It supports popular e-book formats and can automatically organize your files based on author, series, and other metadata.

## Features

- **Read metadata** from e-books including title, author, series info, and ISBN
- **Write/modify metadata** in your e-books
- **Organize your library** by automatically renaming and moving files based on customizable patterns
- **Support for multiple formats**: EPUB, MOBI, AZW and AZW3
- **Intelligent processing** using AI-powered tools to manage your collection

## Installation

```bash
# Install from PyPI
pip install book-strands
```

## Requirements

- Python 3.12 or higher
- [Calibre](https://calibre-ebook.com/) installed

## Usage

```bash
book-strands run /path/to/your/ebooks /path/to/organized/library \
  --output-format "{{author}}/{{series}}/{{title}}.{{extension}}"
```

Output format can be described in plain language as it is an interpreted format.

## Local LLMs

You can also use any local (or remote) Ollama-hosted LLM by setting `--ollama` and configuring it with the below parameters:

```bash
--ollama-model TEXT   Ollama model to use  [default: qwen3:8b]
--ollama-url TEXT     Ollama server URL  [default: http://localhost:11434]
```

### Testing

There are a couple of functions to directly read and write ebook metadata; they are mostly intended for testing purposes if you encounter books that have unusual metadata that causes issues.

#### Read metadata from an e-book

```bash
book-strands read-book /path/to/your/book.epub
```

#### Write metadata to an e-book

```bash
book-strands write-book /path/to/source.epub /path/to/destination.epub \
  --title "New Title" \
  --authors "Author Name, Another Author" \
  --series "Series Name" \
  --series-index "1.0" \
  --description "A super cool book about rad things"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
