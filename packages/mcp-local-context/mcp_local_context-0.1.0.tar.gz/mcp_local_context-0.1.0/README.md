# MCP Local Context

A simple MCP server for local documentation with RAG capabilities. This package provides a simple command to install and use the MCP server for Cursor and Claude that can take a list of folders as sources.

[![PyPI version](https://badge.fury.io/py/mcp-local-context.svg)](https://badge.fury.io/py/mcp-local-context)
[![Python Versions](https://img.shields.io/pypi/pyversions/mcp-local-context.svg)](https://pypi.org/project/mcp-local-context/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This MCP (Model-Context-Protocol) server provides access to local documents stored in source folders, making it easy for AI assistants to access your library documents.

## Features

- **Local Document Access**: Serves document files from your local source folders
- **Multiple Source Folders**: Configure multiple source directories for your documents
- **Document Type Classification**: Automatically categorizes documents as documentation, guides, or conventions
- **Type-Based Filtering**: Search and retrieve documents by specific type
- **Semantic Search**: Find documents based on meaning, not just keywords
- **RAG Implementation**: Uses vector embeddings for document similarity and relevance ranking
- **Directory Listing**: List all available document files
- **Works Offline**: No external API calls - everything is served locally

## Installation

### Requirements

- Python 3.10+
- An MCP-compatible client (Cursor, Claude Desktop, etc.)

### Using pip (recommended)

```bash
# Install from PyPI
pip install mcp-local-context

# Run the server
mcp-local-context
```

To install with RAG capabilities (recommended for semantic search):

```bash
pip install "mcp-local-context[rag]"
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/mcp-local-context.git
```

### Document Organization

Prepare your document files (Markdown, MDX, and text files are supported) and organize them by type:

- **Documentation**: Technical reference material (API docs, class references, etc.)
- **Guides**: How-to content and tutorials
- **Conventions**: Standards, rules, and best practices

## Running the Server

After installing the package, you can run the server with the `mcp-local-context` command:

```bash
# Run with default 'sources' directory
mcp-local-context

# Run with multiple source directories
mcp-local-context docs api-docs specs

# Run with custom host and port
mcp-local-context --host 0.0.0.0 --port 9000

# Run in development mode with the MCP Inspector
mcp-local-context --dev

# Install the server in Claude Desktop
mcp-local-context --install
```

This will:
1. Create the specified source directories if they don't exist
2. Classify your documents by type (documentation, guides, conventions)
3. Build the search index from your document files (if RAG is installed)
4. Start the MCP server (default: http://127.0.0.1:8000/mcp)

## Testing

You can run the tests using the test runner script:

```bash
# Run all tests
python run_tests.py

# Run a specific test
python run_tests.py --test doc_types
python run_tests.py --test client
python run_tests.py --test mcp_sdk

# Start the server before running tests
python run_tests.py --server
```

## Configuration

### Configure for MCP clients

Add to your MCP client configuration file:

<details>
<summary>Cursor Configuration</summary>

Add the following to your Cursor `~/.cursor/mcp.json` file:

```json
"mcpServers": {
  "local-docs": {
    "url": "http://127.0.0.1:8000/mcp"
  }
}
```

Or use the command-based configuration with pip installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "mcp-local-context"
  }
}
```

Or use the command-based configuration with manual installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "./install.sh",
    "args": ["--all"],
    "cwd": "/path/to/mcp-local-context"
  }
}
```
</details>

<details>
<summary>Claude Desktop Configuration</summary>

Add this to your Claude Desktop `claude_desktop_config.json` file:

```json
"mcpServers": {
  "local-docs": {
    "url": "http://127.0.0.1:8000/mcp"
  }
}
```

Or use the command-based configuration with pip installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "mcp-local-context"
  }
}
```

Or use the command-based configuration with manual installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "./install.sh",
    "args": ["--all"],
    "cwd": "/path/to/mcp-local-context"
  }
}
```
</details>

<details>
<summary>VS Code Configuration</summary>

Add this to your VS Code MCP config file:

```json
"servers": {
  "LocalDocs": {
    "type": "streamable-http",
    "url": "http://127.0.0.1:8000/mcp"
  }
}
```
</details>

<details>
<summary>Cline Configuration</summary>

Add this to your Cline configuration file:

```json
"mcpServers": {
  "local-docs": {
    "url": "http://127.0.0.1:8000/mcp"
  }
}
```

Or use the command-based configuration with pip installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "mcp-local-context"
  }
}
```

Or use the command-based configuration with manual installation:

```json
"mcpServers": {
  "local-docs": {
    "command": "./install.sh",
    "args": ["--all"],
    "cwd": "/path/to/mcp-local-context"
  }
}
```
</details>

### Configuring Source Directories

By default, documents are stored in a `sources/` directory in the project folder. You can customize the source directories using command-line arguments or environment variables:

```bash
# Using command-line arguments with manual installation
./install.sh --all docs api-docs specs

# Using command-line arguments with pip installation
mcp-local-context --sources docs api-docs specs

# Using environment variables with manual installation
SOURCE_DIRS="docs api-docs specs" ./install.sh --all

# Using environment variables with pip installation
SOURCE_DIRS="docs api-docs specs" mcp-local-context
```

## Usage

Once configured, you can use the following tools in your AI assistant:

### 1. List Local Documents

To see all available document files:

```
list_local_docs
```

This will return a list of all document files in your configured source folders.

### 2. List Documents by Type

To see all documents of a specific type:

```
list_docs_by_type doc_type="guide"
```

Replace "guide" with the document type you want to list ("documentation", "guide", or "convention").

### 3. Search Local Documents (Path-based)

To search for specific document files by path:

```
search_local_docs query="component"
```

Replace "component" with your search term. This will return a list of files that match your query in their path.

You can also filter by document type:

```
search_local_docs query="component" doc_type="documentation"
```

### 4. Semantic Search (Content-based)

To search for documents based on meaning and content:

```
semantic_search query="How to create a responsive layout"
```

This uses RAG to find the most relevant documents based on the semantic meaning of your query, not just keyword matching. It returns excerpts from the most relevant documents.

You can specify the maximum number of results and filter by document type:

```
semantic_search query="How to handle events" max_results=10 doc_type="guide"
```

### 5. Get Document Content

To retrieve the content of a specific document file:

```
get_local_doc file_path="app-studio/README.md"
```

Replace "app-studio/README.md" with the path to the document file you want to access. The response will include the document's content and its type.

### 6. Build Document Index

If you've added new documents or updated existing files, you can rebuild the search index:

```
build_docs_index
```

This processes all document files, classifies them by type, and creates a new search index for semantic search.

## Adding Your Own Documents

Simply add your Markdown, MDX, or text files to your configured source folders. The server will automatically detect, classify, and serve them.

### Document Type Classification

The server automatically classifies documents based on their content and file path:

1. **Documentation**: Technical reference material (default type if no other type is detected)
2. **Guides**: Files with "guide" in the path or title, or content that appears to be instructional
3. **Conventions**: Files with "convention" in the path or title, or content related to standards/rules

### Organization Tips

For better organization and more accurate classification:

- Use descriptive file names that indicate the document type (e.g., "api-reference.md" for documentation, "getting-started-guide.md" for guides)
- Organize files in subdirectories by type (e.g., `/docs/guides/`, `/docs/conventions/`)
- Use separate source directories for different projects or document categories
- Include clear headings in your documents that indicate their purpose

## Environment Variables

The server can be configured using the following environment variables:

- `SOURCE_DIRS`: Comma-separated list of source directories (e.g., "docs,api-docs,specs")
- `MCP_HOST`: Host to run the server on (default: 127.0.0.1)
- `MCP_PORT`: Port to run the server on (default: 8000)
- `MCP_PATH`: Path for the MCP endpoint (default: /mcp)

## Development

### Setting Up Development Environment

Clone the repository and install development dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-local-context.git
cd mcp-local-context

# Install dependencies using the installation script
./install.sh --install

# Or install in development mode using pip
pip install -e .
```

### Modifying the Server

The main server code is in `docs_server.py`. After making changes, restart the server to apply them.

### Command-Line Options

The server supports the following command-line options:

- `--sources`: List of source folders to index (default: sources)
- `--host`: Host to run the server on (default: 127.0.0.1)
- `--port`: Port to run the server on (default: 8000)
- `--path`: Path for the MCP endpoint (default: /mcp)

### Installation Script Options

The installation script (`install.sh`) supports the following options:

- `-h, --help`: Show help message
- `-i, --install`: Install dependencies
- `-r, --run [source_dirs]`: Run the server with specified source directories
- `-a, --all [source_dirs]`: Install dependencies and run the server (one-step setup)
- `--host [hostname]`: Host to run the server on (default: 127.0.0.1)
- `--port [port]`: Port to run the server on (default: 8000)
- `--path [path]`: Path for the MCP endpoint (default: /mcp)

## License

MIT
