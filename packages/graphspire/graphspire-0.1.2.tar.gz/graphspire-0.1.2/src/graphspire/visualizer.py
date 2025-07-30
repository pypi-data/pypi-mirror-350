"""Module for generating dependency visualizations."""

import os
from typing import Dict, List, Set, Union

from .analyzer import Structure

# Type aliases
NodeId = str
DotContent = str


def sanitize_id(name: str) -> NodeId:
    """Convert a path to a valid Graphviz ID.

    Args:
        name: Path to convert

    Returns:
        Valid Graphviz ID
    """
    return name.replace("/", "_").replace(".", "_").replace("-", "_").replace(" ", "_")


def gather_all_files(structure: Structure, prefix: str = "") -> Set[str]:
    """Gather all files from the structure.

    Args:
        structure: Project structure
        prefix: Current path prefix

    Returns:
        Set of all file paths
    """
    files = set()
    for key, value in structure.items():
        path = os.path.join(prefix, key) if prefix else key
        if isinstance(value, dict):
            files.update(gather_all_files(value, path))
        else:
            files.add(path)
    return files


def generate_mermaid(structure: Structure, parent: str = "root", indent: int = 0) -> List[str]:
    """Generate Mermaid graph lines.

    Args:
        structure: Project structure
        parent: Parent node name
        indent: Current indentation level

    Returns:
        List of Mermaid graph lines
    """
    lines = []
    prefix = "  " * indent
    if isinstance(structure, dict):
        lines.append(f"{prefix}subgraph {parent}")
        for k, v in structure.items():
            if isinstance(v, dict):
                lines.extend(generate_mermaid(v, k, indent + 1))
            else:
                lines.append(f'{prefix}  {k}["{k}"]')
        lines.append(f"{prefix}end")
    return lines


def generate_dependencies(structure: Structure, parent_path: str = "") -> List[str]:
    """Generate dependency lines for Mermaid graph.

    Args:
        structure: Project structure
        parent_path: Current parent path

    Returns:
        List of dependency lines
    """
    deps = []
    if isinstance(structure, dict):
        for k, v in structure.items():
            if isinstance(v, dict):
                deps.extend(generate_dependencies(v, os.path.join(parent_path, k)))
            else:
                src = os.path.join(parent_path, k).replace(os.sep, "/")
                for inc in v:
                    target = inc.replace(os.sep, "/")
                    deps.append(f"{src} --> {target}")
    return deps


def generate_dot(structure: Structure, all_files: Set[str], parent_path: str = "") -> DotContent:
    """Generate Graphviz DOT content.

    Args:
        structure: Project structure
        all_files: Set of all files
        parent_path: Current parent path

    Returns:
        DOT graph content
    """
    dot = ""
    for key, value in structure.items():
        node_path = os.path.join(parent_path, key) if parent_path else key
        node_id = sanitize_id(node_path)
        if isinstance(value, dict):
            # Folder cluster with Catppuccin Latte colors
            dot += f"subgraph cluster_{node_id} {{\n"
            dot += f'label=<<font color="#5c6a72"><b>{key}</b></font>>;\n'  # folder label in latte grey-blue
            dot += "style=filled;\n"
            dot += 'color="#cdd6f4";\n'  # folder border (soft lavender)
            dot += "penwidth=2;\n"
            dot += 'bgcolor="#eff1f5";\n'  # folder bg (latte background)
            dot += "margin=20;\n"
            dot += (
                'node [style=filled, fillcolor="#89b4fa", shape=box, '
                'fontname="JetBrainsMono Nerd Font Mono", fontcolor="#1e1e2e", color="#4c4f69", penwidth=2];\n'
            )
            dot += generate_dot(value, all_files, node_path)
            dot += "}\n"
        else:
            # File node styling (Catppuccin Latte)
            fillcolor = "#89b4fa"  # pastel blue
            bordercolor = "#4c4f69"  # dark grayish blue
            fontcolor = "#1e1e2e"  # very dark text
            dot += (
                f'"{node_id}" [label="{key}", shape=box, style=filled, '
                f'fillcolor="{fillcolor}", color="{bordercolor}", penwidth=2, '
                f'fontname="JetBrainsMono Nerd Font Mono", fontcolor="{fontcolor}"];\n'
            )

            for inc in value:
                # Find all matching included files by name or relative path
                matched_files = [
                    f for f in all_files if os.path.basename(f) == inc or f == inc
                ]
                for mf in matched_files:
                    inc_id = sanitize_id(mf)
                    dot += (
                        f'"{node_id}" -> "{inc_id}" [color="#9399b2", penwidth=1.5, '
                        f"arrowhead=normal, style=solid];\n"
                    )  # muted gray-blue edges
    return dot


def save_mermaid(structure: Structure, output_path: str) -> None:
    """Save Mermaid graph to file.

    Args:
        structure: Project structure
        output_path: Path to save Mermaid file
    """
    mermaid_lines = ["graph TD"]
    mermaid_lines.extend(generate_mermaid(structure))
    mermaid_lines.extend(generate_dependencies(structure))

    with open(output_path, "w") as f:
        f.write("\n".join(mermaid_lines))


def save_dot(structure: Structure, output_path: str) -> None:
    """Save Graphviz DOT graph to file.

    Args:
        structure: Project structure
        output_path: Path to save DOT file
    """
    all_files = gather_all_files(structure)
    dot_content = (
        "digraph Dependencies {\n"
        "compound=true;\n"
        "rankdir=LR;\n"
        "splines=false;\n"  # sharp edges for clarity
        'bgcolor="#303446";\n'  # catppuccin frappe background
        'node [fontname="Arial"];\n'
        'edge [color="#9399b2", penwidth=1.5, arrowhead=normal];\n'  # edges color
    )
    dot_content += generate_dot(structure, all_files)
    dot_content += "}"

    with open(output_path, "w") as f:
        f.write(dot_content) 