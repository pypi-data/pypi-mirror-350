# Long Document MCP Server

[![PyPI version](https://badge.fury.io/py/long-document-mcp.svg)](https://badge.fury.io/py/long-document-mcp)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Model Context Protocol (MCP) server for managing structured long Markdown documents. This server provides tools to create, read, update, and analyze documents composed of multiple chapters.

## Installation

```bash
pip install long-document-mcp
```

## Quick Start

```bash
# Start the MCP server
python -m long_document_mcp.doc_tool_server sse --host localhost --port 3001
```

## Overview

This MCP server treats "long documents" as directories containing multiple "chapter" files (Markdown .md files). Chapters are ordered alphanumerically by their filenames (e.g., `01-introduction.md`, `02-main_content.md`).

### Document Structure

```
long_documents_storage/           # Root directory for all documents
├── my_book/                     # A long document (directory)
│   ├── 01-introduction.md       # Chapter 1 (alphanumeric ordering)
│   ├── 02-main_content.md       # Chapter 2
│   ├── 03-conclusion.md         # Chapter 3
│   └── _manifest.json           # Optional: For future explicit chapter ordering
└── research_paper/              # Another long document
    ├── 00-abstract.md
    ├── 01-methodology.md
    └── 02-results.md
```

## Configuration

The server uses the following environment variables:

- `LONG_DOCUMENT_ROOT_DIR`: Root directory for storing documents (default: `long_documents_storage/`)

## Running the Server

The server supports both HTTP SSE and stdio transports. HTTP SSE is the default and recommended transport.

### HTTP SSE Transport (Recommended)

```bash
# Run with HTTP SSE transport (default)
python -m long_document_mcp.doc_tool_server sse --host localhost --port 3001

# Or specify arguments explicitly
python -m long_document_mcp.doc_tool_server sse --host 0.0.0.0 --port 8000
```

### Stdio Transport

```bash
# Run with stdio transport
python -m long_document_mcp.doc_tool_server stdio
```

## MCP Tools Reference

The server exposes the following tools via the Model Context Protocol:

### Document Management

| Tool | Parameters | Description |
|------|------------|-------------|
| `list_long_documents` | - | Lists all available long documents with metadata |
| `create_long_document` | `document_name: str` | Creates a new long document directory |
| `delete_long_document` | `document_name: str` | Deletes a long document and all its chapters |

### Chapter Management

| Tool | Parameters | Description |
|------|------------|-------------|
| `list_chapters` | `document_name: str` | Lists all chapters in a document, ordered by filename |
| `create_chapter` | `document_name: str`, `chapter_name: str`, `initial_content: str = ""` | Creates a new chapter file |
| `delete_chapter` | `document_name: str`, `chapter_name: str` | Deletes a chapter from a document |

### Content Operations

| Tool | Parameters | Description |
|------|------------|-------------|
| `read_chapter_content` | `document_name: str`, `chapter_name: str` | Reads the content and metadata of a specific chapter |
| `read_paragraph_content` | `document_name: str`, `chapter_name: str`, `paragraph_index_in_chapter: int` | Reads a specific paragraph from a chapter |
| `read_full_long_document` | `document_name: str` | Reads the entire document, concatenating all chapters |
| `write_chapter_content` | `document_name: str`, `chapter_name: str`, `new_content: str` | Overwrites the entire content of a chapter |
| `modify_paragraph_content` | `document_name: str`, `chapter_name: str`, `paragraph_index: int`, `new_paragraph_content: str`, `mode: str` | Modifies a paragraph (`replace`, `insert_before`, `insert_after`, `delete`) |
| `append_paragraph_to_chapter` | `document_name: str`, `chapter_name: str`, `paragraph_content: str` | Appends a new paragraph to the end of a chapter |

### Text Operations

| Tool | Parameters | Description |
|------|------------|-------------|
| `replace_text_in_chapter` | `document_name: str`, `chapter_name: str`, `text_to_find: str`, `replacement_text: str` | Replaces all occurrences of text in a specific chapter |
| `replace_text_in_document` | `document_name: str`, `text_to_find: str`, `replacement_text: str` | Replaces all occurrences of text throughout all chapters |

### Analysis Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `get_chapter_statistics` | `document_name: str`, `chapter_name: str` | Retrieves statistics (word count, paragraph count) for a chapter |
| `get_document_statistics` | `document_name: str` | Retrieves aggregated statistics for an entire document |

### Search Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| `find_text_in_chapter` | `document_name: str`, `chapter_name: str`, `query: str`, `case_sensitive: bool = False` | Finds paragraphs containing the query string in a specific chapter |
| `find_text_in_document` | `document_name: str`, `query: str`, `case_sensitive: bool = False` | Finds paragraphs containing the query string across all chapters |

## Data Models

The server uses Pydantic models for structured data exchange:

- `LongDocumentInfo`: Metadata for a long document
- `ChapterMetadata`: Metadata for a chapter
- `ChapterContent`: Full content and metadata of a chapter
- `ParagraphDetail`: Information about a specific paragraph
- `FullLongDocumentContent`: Complete content of a document
- `StatisticsReport`: Word and paragraph count statistics
- `OperationStatus`: Success/failure status for operations

## Requirements

- Python 3.8+
- fastapi
- uvicorn[standard]
- pydantic-ai
- mcp[cli]
- python-dotenv
- google-generativeai

## Examples and Documentation

For comprehensive examples, tutorials, and usage guides, visit the [GitHub repository](https://github.com/long-document-mcp/long-document-mcp).

## License

MIT License

## Links

- **GitHub Repository**: [https://github.com/long-document-mcp/long-document-mcp](https://github.com/long-document-mcp)
- **Bug Reports**: [GitHub Issues](https://github.com/long-document-mcp/issues) 