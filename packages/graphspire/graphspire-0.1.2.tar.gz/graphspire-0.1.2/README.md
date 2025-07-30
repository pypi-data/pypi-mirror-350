# GraphSpire

A tool to analyze and visualize C++ project dependencies. It generates beautiful dependency graphs from your C++ project's include statements.

## Features

- Analyzes C++ project structure and include dependencies
- Generates multiple visualization formats:
  - JSON structure for programmatic use
  - Mermaid graph for documentation
  - Graphviz DOT for high-quality visualizations
- Respects `.gitignore` patterns
- Customizable ignore patterns
- Beautiful Catppuccin-themed visualizations

## Installation

```bash
# Install from PyPI
pip install graphspire

# Or install from source
git clone https://github.com/kshitijaucharmal/graphspire.git
cd graphspire
pip install -e .
```

## Usage

Basic usage:
```bash
graphspire --dir /path/to/cpp/project
```

Advanced usage:
```bash
graphspire \
    --dir /path/to/cpp/project \
    --ignore "build/" "external/" \
    --output-json deps.json \
    --output-mermaid deps.mmd \
    --output-dot deps.dot \
    --verbose
```

### Command Line Options

- `--dir`: Target directory to analyze (default: current directory)
- `--output-json`: Output JSON file (default: project_structure.json)
- `--output-mermaid`: Output Mermaid file (default: dependencies.mmd)
- `--output-dot`: Output DOT file (default: dependencies.dot)
- `--ignore-gitignore`: Ignore .gitignore file
- `--ignore`: Explicit folders or files to ignore (supports patterns)
- `--verbose`: Enable verbose output

### Rendering the DOT File

To render the DOT file into a PNG:
```bash
dot -Tpng -Gdpi=300 -Gsize=10,10 dependencies.dot -o graph.png
```

## Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest
   ```
