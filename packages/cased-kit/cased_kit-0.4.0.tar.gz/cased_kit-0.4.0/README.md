# kit 🛠️ Code Intelligence Toolkit


<img src="https://github.com/user-attachments/assets/7bdfa9c6-94f0-4ee0-9fdd-cbd8bd7ec060" width="360">

`kit` is a production-ready toolkit for codebase mapping, symbol extraction, code search, and building LLM-powered developer tools, agents, and workflows. 

Use `kit` to build things like code reviewers, code generators, even IDEs, all enriched with the right code context.

Work with `kit` directly from Python, or with MCP + function calling, REST, or CLI!

## Quick Installation

### Install from PyPI

```bash
# Standard installation (all features, including the kit-mcp server)
pip install cased-kit
```

### Install from Source

```bash
git clone https://github.com/cased/kit.git
cd kit
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

## Basic Usage

### Python API

```python
from kit import Repository

# Load a local repository
repo = Repository("/path/to/your/local/codebase")

# Load a remote public GitHub repo
# repo = Repository("https://github.com/owner/repo")

# Load a repository at a specific commit, tag, or branch
# repo = Repository("https://github.com/owner/repo", ref="v1.2.3")

# Explore the repo
print(repo.get_file_tree())
# Output: [{"path": "src/main.py", "is_dir": False, ...}, ...]

print(repo.extract_symbols('src/main.py'))
# Output: [{"name": "main", "type": "function", "file": "src/main.py", ...}, ...]

# Access git metadata
print(f"Current SHA: {repo.current_sha}")
print(f"Branch: {repo.current_branch}")
```

### Command Line Interface

`kit` also provides a comprehensive CLI for repository analysis and code exploration:

```bash
# Get repository file structure
kit file-tree /path/to/repo

# Extract symbols (functions, classes, etc.)
kit symbols /path/to/repo --format table

# Search for code patterns
kit search /path/to/repo "def main" --pattern "*.py"

# Find symbol usages
kit usages /path/to/repo "MyClass"

# Export data for external tools
kit export /path/to/repo symbols symbols.json
```

The CLI supports all major repository operations with Unix-friendly output for scripting and automation. See the [CLI Documentation](https://kit.cased.com/introduction/cli) for comprehensive usage examples.

## Key Features & Capabilities

`kit` helps your apps and agents understand and interact with codebases, with components to build your own AI-powered developer tools.

*   **Explore Code Structure:**
    *   High-level view with `repo.get_file_tree()` to list all files and directories.
    *   Dive down with `repo.extract_symbols()` to identify functions, classes, and other code constructs, either across the entire repository or within a single file.

*   **Pinpoint Information:**
    *   Run regular expression searches across your codebase using `repo.search_text()`.
    *   Track specific symbols (like a function or class) with `repo.find_symbol_usages()`.
    *   Perform semantic code search using vector embeddings to find code based on meaning rather than just keywords.

*   **Prepare Code for LLMs & Analysis:**
    *   Break down large files into manageable pieces for LLM context windows using `repo.chunk_file_by_lines()` or `repo.chunk_file_by_symbols()`.
    *   Get the full definition of a function or class off a line number within it using `repo.extract_context_around_line()`.

*   **Generate Code Summaries:**
    *   Use LLMs to create natural language summaries for files, functions, or classes using the `Summarizer` (e.g., `summarizer.summarize_file()`, `summarizer.summarize_function()`).
    *   Build a searchable semantic index of these AI-generated docstrings with `DocstringIndexer` and query it with `SummarySearcher` to find code based on intent and meaning.

*   **Analyze Code Dependencies:**
    *   Map import relationships between modules using `repo.get_dependency_analyzer()` to understand your codebase structure.
    *   Generate dependency reports and LLM-friendly context with `analyzer.generate_dependency_report()` and `analyzer.generate_llm_context()`.

*   **Repository Versioning & Historical Analysis:**
    *   Analyze repositories at specific commits, tags, or branches using the `ref` parameter.
    *   Compare code evolution over time, work with diffs, ensure reproducible analysis results
    *   Access git metadata including current SHA, branch, and remote URL with `repo.current_sha`, `repo.current_branch`, etc.

*   **Multiple Access Methods:**
    *   **Python API**: Direct integration for building applications and scripts.
    *   **Command Line Interface**: 11+ commands for shell scripting, CI/CD, and automation workflows.
    *   **REST API**: HTTP endpoints for web applications and microservices.
    *   **MCP Server**: Model Context Protocol integration for AI agents and development tools.

## MCP Server

The `kit` tool includes an MCP (Model Context Protocol) server that allows AI agents and other development tools to interact with a codebase programmatically.

MCP support is currently in alpha. Add a stanza like this to your MCP tool:

```jsonc
{
  "mcpServers": {
    "kit-mcp": {
      "command": "python",
      "args": ["-m", "kit.mcp"]
    }
  }
}
```

The `python` executable invoked must be the one where `cased-kit` is installed.
If you see `ModuleNotFoundError: No module named 'kit'`, ensure the Python
interpreter your MCP client is using is the correct one.


## Documentation

Explore the **[Full Documentation](https://kit.cased.com)** for detailed usage, advanced features, and practical examples.
Full REST documentation is also available.


## License

MIT License

## Contributing

- **Local Development**: Check out our [Running Tests](https://kit.cased.com/development/running-tests) guide to get started with local development.
- **Project Direction**: See our [Roadmap](https://kit.cased.com/development/roadmap) for future plans and focus areas.

To contribute, fork the repository, make your changes, and submit a pull request.

