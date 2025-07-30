"""Tests for the visualizer module."""

import os
import tempfile
from pathlib import Path

import pytest

from graphspire.analyzer import Structure
from graphspire.visualizer import (
    gather_all_files,
    generate_dependencies,
    generate_dot,
    generate_mermaid,
    sanitize_id,
)


@pytest.fixture
def sample_structure() -> Structure:
    """Create a sample project structure."""
    return {
        "src": {
            "main.cpp": ["header.hpp", "../include/other.hpp"],
            "utils.cpp": ["utils.hpp"],
        },
        "include": {
            "header.hpp": ["other.hpp"],
            "utils.hpp": [],
            "other.hpp": [],
        },
    }


def test_sanitize_id():
    """Test ID sanitization."""
    assert sanitize_id("path/to/file.hpp") == "path_to_file_hpp"
    assert sanitize_id("my-file.cpp") == "my_file_cpp"
    assert sanitize_id("space in name.hpp") == "space_in_name_hpp"


def test_gather_all_files(sample_structure):
    """Test file gathering."""
    files = gather_all_files(sample_structure)
    assert len(files) == 5
    assert "src/main.cpp" in files
    assert "src/utils.cpp" in files
    assert "include/header.hpp" in files
    assert "include/utils.hpp" in files
    assert "include/other.hpp" in files


def test_generate_mermaid(sample_structure):
    """Test Mermaid graph generation."""
    lines = generate_mermaid(sample_structure)
    assert "subgraph src" in lines
    assert "subgraph include" in lines
    assert 'main.cpp["main.cpp"]' in lines
    assert 'header.hpp["header.hpp"]' in lines


def test_generate_dependencies(sample_structure):
    """Test dependency generation."""
    deps = generate_dependencies(sample_structure)
    assert "src/main.cpp --> header.hpp" in deps
    assert "src/main.cpp --> ../include/other.hpp" in deps
    assert "include/header.hpp --> other.hpp" in deps


def test_generate_dot(sample_structure):
    """Test DOT graph generation."""
    all_files = gather_all_files(sample_structure)
    dot = generate_dot(sample_structure, all_files)
    assert "digraph" not in dot  # Should not include graph declaration
    assert "subgraph cluster_src" in dot
    assert "subgraph cluster_include" in dot
    assert 'label="main.cpp"' in dot
    assert 'label="header.hpp"' in dot 