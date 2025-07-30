# Long Document MCP

A Model Context Protocol (MCP) server and example agent for managing structured long Markdown documents.

## Overview

This project provides:

1. **Long Document MCP Server** (`long_document_mcp/`): A MCP server that manages "long documents" as directories containing multiple "chapter" files (Markdown .md files)
2. **Example Agent** (`examples/`): A Pydantic AI agent that demonstrates how to use the MCP server with natural language queries

## Project Structure

```
.
├── long_document_mcp/           # MCP server package
│   ├── __init__.py
│   ├── doc_tool_server.py       # Main MCP server implementation
│   ├── agent.py                 # Agent implementation (included in package)
│   ├── test_doc_tool_server.py  # MCP server tests
│   ├── conftest.py              # Package test configuration
│   ├── pytest.ini              # Package pytest settings
│   └── README.md                # MCP server documentation
├── examples/                    # Example usage
│   ├── agent.py                 # Example Pydantic AI agent
│   ├── test_agent.py            # Agent tests
│   ├── conftest.py              # Example test configuration
│   └── README.md                # Agent example documentation
├── pyproject.toml               # Package configuration
├── pytest.ini                  # Main pytest settings (for examples)
├── run_tests.py                 # Test runner script
├── requirements.txt             # Development dependencies
└── README.md                    # This file
```

## Installation

Install the MCP server package:

```bash
pip install long-document-mcp
```

## Quick Start

### Using the MCP Server

The MCP server can be used with any MCP client. It provides tools for managing structured Markdown documents.

See [`long_document_mcp/README.md`](long_document_mcp/README.md) for detailed MCP server documentation.

### Using the Example Agent

The example agent demonstrates how to build an AI assistant that uses the MCP server:

```bash
# Install the package
pip install long-document-mcp

# Run the example agent
long-document-mcp
```

See [`examples/README.md`](examples/README.md) for detailed agent documentation and examples.

## Document Structure

Long documents are organized as directories containing chapter files:

```
long_documents_storage/           # Root directory
├── my_book/                     # A long document
│   ├── 01-introduction.md       # Chapter 1
│   ├── 02-main_content.md       # Chapter 2
│   └── 03-conclusion.md         # Chapter 3
└── research_paper/              # Another document
    ├── 00-abstract.md
    └── 01-methodology.md
```

## Development

### Setup

```bash
git clone <repository>
cd long-document-mcp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Testing

```bash
# Test the MCP server (from package directory)
cd long_document_mcp
pytest test_doc_tool_server.py -v

# Test the example agent (from project root)
cd ..
pytest examples/test_agent.py -v

# Or run all example tests
pytest -v

# Run all tests with the test runner script
python run_tests.py
```

### Building and Publishing

```bash
# Build the package
python -m build

# Publish to PyPI (requires authentication)
twine upload dist/*
```

## Features

### MCP Server Tools

- **Document Management**: Create, list, delete documents
- **Chapter Management**: Create, list, delete, read chapters
- **Content Operations**: Read, write, modify paragraphs
- **Text Operations**: Find and replace text
- **Analysis**: Get statistics, search content

### Example Agent Features

- **Natural Language Interface**: Understands various ways to express document operations
- **Structured Responses**: Consistent output format using Pydantic models
- **Error Handling**: Graceful handling of errors and edge cases
- **Extensible**: Easy to customize and extend with new capabilities

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request