"""Command-line interface for dependency-chart."""

import argparse
import logging
import os
import sys
import subprocess
from pathlib import Path

from .analyzer import build_structure, load_gitignore, save_structure
from .visualizer import save_dot, save_mermaid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def get_default_storage_dir(project_name: str) -> Path:
    """Get the default storage directory for a project.

    Args:
        project_name: Name of the project

    Returns:
        Path to the storage directory
    """
    home = Path.home()
    storage_dir = home / ".graphspire" / project_name
    storage_dir.mkdir(parents=True, exist_ok=True)
    return storage_dir


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments
    """
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
        "--storage-dir",
        type=str,
        help="Custom storage directory (default: ~/.graphspire/<project_name>)",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default="project_structure.json",
        help="Output JSON file name (default: project_structure.json)",
    )
    parser.add_argument(
        "--output-mermaid",
        type=str,
        default="dependencies.mmd",
        help="Output Mermaid file name (default: dependencies.mmd)",
    )
    parser.add_argument(
        "--output-dot",
        type=str,
        default="dependencies.dot",
        help="Output DOT file name (default: dependencies.dot)",
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
    parser.add_argument(
        "--open-xdot",
        action="store_true",
        help="Open the generated graph in xdot",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Get absolute path
    project_root = os.path.abspath(args.dir)
    project_name = os.path.basename(project_root)
    logger.info(f"Analyzing project in: {project_root}")

    # Determine storage directory
    if args.storage_dir:
        storage_dir = Path(args.storage_dir)
    else:
        storage_dir = get_default_storage_dir(project_name)
    logger.info(f"Using storage directory: {storage_dir}")

    # Load ignore patterns
    ignored_patterns = set()
    if not args.ignore_gitignore:
        ignored_patterns = load_gitignore(project_root)
        if ignored_patterns and args.verbose:
            logger.debug(f"Loaded .gitignore patterns: {ignored_patterns}")

    try:
        # Build structure
        tree = build_structure(
            project_root,
            ignored_patterns,
            explicit_ignores=set(args.ignore),
            verbose=args.verbose,
        )

        # Save outputs
        json_path = storage_dir / args.output_json
        save_structure(tree, str(json_path))

        mmd_path = storage_dir / args.output_mermaid
        save_mermaid(tree, str(mmd_path))
        logger.info(f"Saved Mermaid graph to {mmd_path}")

        dot_path = storage_dir / args.output_dot
        save_dot(tree, str(dot_path))
        logger.info(f"Generated Graphviz DOT file: {dot_path}")

        # Open in xdot if requested
        if args.open_xdot:
            try:
                subprocess.run(["xdot", str(dot_path)], check=True)
            except subprocess.CalledProcessError:
                logger.error("Failed to open xdot. Make sure it's installed.")
            except FileNotFoundError:
                logger.error("xdot not found. Please install it first.")
        else:
            logger.info("To view the graph:")
            logger.info(f"  xdot {dot_path}")
            logger.info("To render as PNG with good quality:")
            logger.info(f"  dot -Tpng -Gdpi=300 -Gsize=10,10 {dot_path} -o {storage_dir}/graph.png")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 