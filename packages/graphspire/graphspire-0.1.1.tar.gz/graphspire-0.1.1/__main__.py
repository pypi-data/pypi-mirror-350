import os
import re
import json
import argparse
from pathlib import Path
from dependency_analyzer import (
    build_structure,
    load_gitignore,
    generate_mermaid,
    generate_dependencies,
    generate_dot,
    gather_all_files,
)

include_pattern = re.compile(r'#include\s+"(.+?)"')


def extract_includes(file_path):
    includes = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = include_pattern.search(line)
            if match:
                includes.append(match.group(1))
    return includes


def is_ignored(path, ignored_patterns, explicit_ignores):
    for pattern in ignored_patterns.union(explicit_ignores):
        if Path(path).match(pattern):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Analyze C++ project includes and generate dependency visualizations."
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Target directory (default: current directory)",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="project_structure.json",
        help="Output JSON file (default: project_structure.json)",
    )
    parser.add_argument(
        "--output-mermaid",
        type=str,
        default="dependencies.mmd",
        help="Output Mermaid file (default: dependencies.mmd)",
    )
    parser.add_argument(
        "--output-dot",
        type=str,
        default="dependencies.dot",
        help="Output DOT file (default: dependencies.dot)",
    )
    parser.add_argument(
        "--ignore-gitignore", action="store_true", help="Ignore .gitignore file"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="Explicit folders or files to ignore (supports patterns)",
    )

    args = parser.parse_args()

    project_root = os.path.abspath(args.dir)
    print(f"Analyzing project in: {project_root}")

    ignored_patterns = set()
    if not args.ignore_gitignore:
        ignored_patterns = load_gitignore(project_root)
        if ignored_patterns and args.verbose:
            print(f"Loaded .gitignore patterns: {ignored_patterns}")

    tree = build_structure(
        project_root,
        ignored_patterns,
        explicit_ignores=set(args.ignore),
        verbose=args.verbose,
    )

    # Save to JSON
    json_path = os.path.join(project_root, args.output_json)
    with open(json_path, "w") as jf:
        json.dump(tree, jf, indent=2)
    print(f"Saved JSON to {json_path}")

    # Generate Mermaid
    mermaid_lines = ["graph TD"]
    mermaid_lines.extend(generate_mermaid(tree))
    mermaid_lines.extend(generate_dependencies(tree))

    mmd_path = os.path.join(project_root, args.output_mermaid)
    with open(mmd_path, "w") as mf:
        mf.write("\n".join(mermaid_lines))
    print(f"Saved Mermaid graph to {mmd_path}")

    # Generate DOT
    all_files = gather_all_files(tree)
    dot_content = (
        "digraph Dependencies {\n"
        "compound=true;\n"
        "rankdir=LR;\n"
        "splines=false;\n"  # sharp edges for clarity
        'bgcolor="#303446";\n'  # catppuccin frappe background
        'node [fontname="Arial"];\n'
        'edge [color="#9399b2", penwidth=1.5, arrowhead=normal];\n'  # edges color
    )
    dot_content += generate_dot(tree, all_files)
    dot_content += "}"

    dot_path = os.path.join(project_root, args.output_dot)
    with open(dot_path, "w") as f:
        f.write(dot_content)
    print(f"Generated Graphviz DOT file: {dot_path}")
    print("To render as PNG with good quality:")
    print(f"  dot -Tpng -Gdpi=300 -Gsize=10,10 {dot_path} -o graph.png")
    print("View with an image viewer or use 'xdot graph.png' for interactive viewing.")


if __name__ == "__main__":
    main()
