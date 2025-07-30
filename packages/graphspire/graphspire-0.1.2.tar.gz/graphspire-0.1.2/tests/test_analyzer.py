"""Tests for the analyzer module."""

import os
import tempfile
from pathlib import Path

import pytest

from graphspire.analyzer import (
    build_structure,
    extract_includes,
    is_ignored,
    load_gitignore,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        os.makedirs(os.path.join(tmpdir, "src"))
        os.makedirs(os.path.join(tmpdir, "include"))

        # Create a .gitignore file
        with open(os.path.join(tmpdir, ".gitignore"), "w") as f:
            f.write("build/\n*.o\n")

        # Create some C++ files
        with open(os.path.join(tmpdir, "src", "main.cpp"), "w") as f:
            f.write('#include "header.hpp"\n')
            f.write('#include "../include/other.hpp"\n')

        with open(os.path.join(tmpdir, "include", "header.hpp"), "w") as f:
            f.write('#include "other.hpp"\n')

        with open(os.path.join(tmpdir, "include", "other.hpp"), "w") as f:
            f.write("// Empty header\n")

        yield tmpdir


def test_extract_includes(temp_dir):
    """Test include extraction."""
    main_cpp = os.path.join(temp_dir, "src", "main.cpp")
    includes = extract_includes(main_cpp)
    assert len(includes) == 2
    assert "header.hpp" in includes
    assert "../include/other.hpp" in includes


def test_load_gitignore(temp_dir):
    """Test .gitignore loading."""
    patterns = load_gitignore(temp_dir)
    assert "build/" in patterns
    assert "*.o" in patterns


def test_is_ignored():
    """Test ignore pattern matching."""
    patterns = {"build/", "*.o"}
    explicit = {"test/"}
    assert is_ignored("build/file.txt", patterns, explicit)
    assert is_ignored("file.o", patterns, explicit)
    assert is_ignored("test/file.txt", patterns, explicit)
    assert not is_ignored("src/file.cpp", patterns, explicit)


def test_build_structure(temp_dir):
    """Test structure building."""
    structure = build_structure(temp_dir, set(), set())
    assert "src" in structure
    assert "include" in structure
    assert "main.cpp" in structure["src"]
    assert "header.hpp" in structure["include"]
    assert "other.hpp" in structure["include"] 