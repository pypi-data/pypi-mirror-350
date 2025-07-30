import os
import re
import json
from pathlib import Path

include_pattern = re.compile(r'#include\s+"(.+?)"')

def extract_includes(file_path):
    includes = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = include_pattern.search(line)
            if match:
                includes.append(match.group(1))
    return includes

def load_gitignore(root_path):
    gitignore_path = os.path.join(root_path, ".gitignore")
    ignored = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored.add(line)
    return ignored

def is_ignored(path, ignored_patterns, explicit_ignores):
    for pattern in ignored_patterns.union(explicit_ignores):
        if Path(path).match(pattern):
            return True
    return False

def build_structure(path, ignored_patterns, explicit_ignores, verbose=False):
    structure = {}
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        # Always skip .git folder
        if ".git" in rel_root.split(os.sep):
            if verbose:
                print(f"Skipping .git directory: {rel_root}")
            continue
        if is_ignored(rel_root, ignored_patterns, explicit_ignores):
            if verbose:
                print(f"Skipping ignored directory: {rel_root}")
            continue
        node = structure
        if rel_root != ".":
            for part in rel_root.split(os.sep):
                node = node.setdefault(part, {})
        # Filter dirs in-place to respect ignore patterns + skip .git
        dirs[:] = [
            d
            for d in dirs
            if d != ".git"
            and not is_ignored(
                os.path.join(rel_root, d), ignored_patterns, explicit_ignores
            )
        ]
        for f in files:
            if is_ignored(
                os.path.join(rel_root, f), ignored_patterns, explicit_ignores
            ):
                if verbose:
                    print(f"Skipping ignored file: {os.path.join(rel_root, f)}")
                continue
            if f.endswith((".cpp", ".hpp")):
                full_path = os.path.join(root, f)
                node[f] = extract_includes(full_path)
    return structure

def generate_mermaid(structure, parent="root", indent=0):
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

def generate_dependencies(structure, parent_path=""):
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

def sanitize_id(name):
    # Graphviz IDs can't have certain characters
    return name.replace("/", "_").replace(".", "_").replace("-", "_").replace(" ", "_")

def gather_all_files(structure, prefix=""):
    files = set()
    for key, value in structure.items():
        path = os.path.join(prefix, key) if prefix else key
        if isinstance(value, dict):
            files.update(gather_all_files(value, path))
        else:
            files.add(path)
    return files

def generate_dot(structure, all_files, parent_path=""):
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