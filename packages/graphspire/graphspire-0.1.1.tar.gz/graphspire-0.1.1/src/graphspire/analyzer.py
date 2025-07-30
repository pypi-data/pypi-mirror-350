"""Core module for analyzing C++ project dependencies."""

import json
import logging
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Union

# Configure logging
logger = logging.getLogger(__name__)

# Type aliases
Structure = Dict[str, Union[Dict[str, "Structure"], List[str]]]
IncludePattern = re.Pattern

# Constants
INCLUDE_PATTERN: IncludePattern = re.compile(r'#include\s+"(.+?)"')
CPP_EXTENSIONS = (".cpp", ".hpp", ".h", ".cc", ".cxx")


def extract_includes(file_path: str) -> List[str]:
    """Extract include statements from a C++ file.

    Args:
        file_path: Path to the C++ file

    Returns:
        List of included file paths
    """
    includes = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = INCLUDE_PATTERN.search(line)
                if match:
                    includes.append(match.group(1))
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
    return includes


def load_gitignore(root_path: str) -> Set[str]:
    """Load patterns from .gitignore file.

    Args:
        root_path: Path to the project root

    Returns:
        Set of ignore patterns
    """
    gitignore_path = os.path.join(root_path, ".gitignore")
    ignored = set()
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        ignored.add(line)
        except Exception as e:
            logger.error(f"Error reading .gitignore: {e}")
    return ignored


def is_ignored(path: str, ignored_patterns: Set[str], explicit_ignores: Set[str]) -> bool:
    """Check if a path should be ignored.

    Args:
        path: Path to check
        ignored_patterns: Patterns from .gitignore
        explicit_ignores: Explicit ignore patterns

    Returns:
        True if path should be ignored
    """
    path_obj = Path(path)
    for pattern in ignored_patterns.union(explicit_ignores):
        try:
            if path_obj.match(pattern):
                return True
        except Exception:
            # Skip invalid patterns
            continue
    return False


def build_structure(
    path: str,
    ignored_patterns: Set[str],
    explicit_ignores: Set[str],
    verbose: bool = False,
) -> Structure:
    """Build the project structure with dependencies.

    Args:
        path: Root path of the project
        ignored_patterns: Patterns from .gitignore
        explicit_ignores: Explicit ignore patterns
        verbose: Enable verbose logging

    Returns:
        Nested dictionary representing project structure
    """
    structure: Structure = {}
    path_obj = Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Project directory not found: {path}")

    if not path_obj.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)
        
        # Skip .git directory
        if ".git" in rel_root.split(os.sep):
            if verbose:
                logger.info(f"Skipping .git directory: {rel_root}")
            continue

        # Skip ignored directories
        if is_ignored(rel_root, ignored_patterns, explicit_ignores):
            if verbose:
                logger.info(f"Skipping ignored directory: {rel_root}")
            continue

        # Build structure
        node = structure
        if rel_root != ".":
            for part in rel_root.split(os.sep):
                node = node.setdefault(part, {})

        # Filter directories
        dirs[:] = [
            d
            for d in dirs
            if d != ".git"
            and not is_ignored(
                os.path.join(rel_root, d), ignored_patterns, explicit_ignores
            )
        ]

        # Process files
        for f in files:
            if is_ignored(
                os.path.join(rel_root, f), ignored_patterns, explicit_ignores
            ):
                if verbose:
                    logger.info(f"Skipping ignored file: {os.path.join(rel_root, f)}")
                continue

            if f.endswith(CPP_EXTENSIONS):
                full_path = os.path.join(root, f)
                node[f] = extract_includes(full_path)

    if not structure:
        logger.warning("No C++ files found in the project directory.")

    return structure


def save_structure(structure: Structure, output_path: str) -> None:
    """Save project structure to JSON file.

    Args:
        structure: Project structure to save
        output_path: Path to save JSON file
    """
    try:
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(structure, f, indent=2)
        logger.info(f"Saved structure to {output_path}")
    except Exception as e:
        logger.error(f"Error saving structure to {output_path}: {e}")
        raise 