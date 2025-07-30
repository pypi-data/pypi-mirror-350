# GraphSpire

<div align="center">
  <img src="assets/graphspire_banner.png" alt="GraphSpire Banner" width="800"/>
</div>

A tool to analyze and visualize C++ project dependencies. It generates beautiful dependency graphs from your C++ project's include statements.

## Why GraphSpire?

Ever found yourself lost in a maze of C++ includes? GraphSpire helps you navigate through complex C++ projects by generating clear, beautiful dependency graphs. Whether you're refactoring legacy code or starting a new project, GraphSpire gives you the bird's-eye view you need.

## Features

- Analyzes C++ project structure and include dependencies
- Generates multiple visualization formats:
  - JSON structure for programmatic use
  - Mermaid graph for documentation
  - Graphviz DOT for high-quality visualizations
- Respects `.gitignore` patterns
- Customizable ignore patterns
- Beautiful Catppuccin-themed visualizations

## Quick Start

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

Want to contribute? Awesome! Here's how to get started:

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

## License

MIT License - feel free to use this in your projects!

## Contributing

Found a bug? Have a feature request? Contributions are welcome! Feel free to open an issue or submit a pull request.

---

<div align="center">
  <img src="assets/graphspire_logo.png" alt="GraphSpire Logo" width="100"/>
  <br/>
  <sub>Built for the C++ community</sub>
</div>
