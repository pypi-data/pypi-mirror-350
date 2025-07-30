"""GraphSpire - A tool to analyze and visualize C++ project dependencies."""

from .analyzer import build_structure, load_gitignore, save_structure
from .visualizer import save_dot, save_mermaid
from .cli import main

__version__ = "0.1.0"

__all__ = [
    "build_structure",
    "load_gitignore",
    "save_structure",
    "save_dot",
    "save_mermaid",
    "main",
    "__version__",
] 