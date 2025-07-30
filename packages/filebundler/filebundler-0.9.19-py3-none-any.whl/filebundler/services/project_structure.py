# filebundler/services/project_structure.py
import sys
import logging
import logfire

from pathlib import Path

from filebundler.models.FileItem import FileItem
from filebundler.FileBundlerApp import FileBundlerApp

logger = logging.getLogger(__name__)


def _generate_project_structure(app: FileBundlerApp):
    """
    Generate a markdown representation of the project structure

    Args:
        file_items: Dictionary of FileItem objects
        project_path: Root path of the project

    Returns:
        str: Markdown representation of the project structure
    """
    try:
        with logfire.span(
            "generating project structure for {project_name}",
            project_name=app.project_path.name,
        ):
            project_name = app.project_path.name
            logger.info(
                f"Generating project structure for {project_name} ({app.project_path = })"
            )
            structure_markdown = [f"# Project Structure: {project_name}\n"]

            structure_markdown.append("## Directory Structure\n```\n")

            # Get the root item
            if not app.root_item:
                logger.error(f"Root item not found for {app.project_path}")
                return "Error: Root directory not found in file items"

            # Recursive function to build the directory tree
            def build_tree(directory_item: FileItem, prefix: str = "") -> list[str]:
                with logfire.span(
                    "building tree for {directory}", directory=directory_item.name
                ):
                    result: list[str] = []

                    # Sort children: directories first, then files, all alphabetically
                    sorted_children = sorted(
                        directory_item.children,
                        key=lambda x: (not x.is_dir, x.name.lower()),
                    )

                    for i, child in enumerate(sorted_children):
                        is_last = i == len(sorted_children) - 1

                        # Choose the proper prefix for the current item
                        curr_prefix = "└── " if is_last else "├── "

                        # Choose the proper prefix for the next level
                        next_prefix = "    " if is_last else "│   "

                        if child.is_dir:
                            result.append(
                                f"{prefix}{curr_prefix}📁 {child.name}/ ({child.tokens} tokens)"
                            )
                            subtree = build_tree(child, prefix + next_prefix)
                            result.extend(subtree)
                        else:
                            result.append(
                                f"{prefix}{curr_prefix}📄 {child.name} ({child.tokens} tokens)"
                            )

                    return result

            # Generate tree starting from root
            tree_lines = build_tree(app.root_item)
            structure_markdown.append(
                f"{app.project_path.name}/ ({app.root_item.tokens})\n"
            )
            structure_markdown.extend([f"{line}\n" for line in tree_lines])
            structure_markdown.append("```\n")

            return "".join(structure_markdown)

    except Exception as e:
        logger.error(f"Error generating project structure: {e}", exc_info=True)
        return f"Error generating project structure: {str(e)}"


# TODO make asynchronous
def save_project_structure(app: FileBundlerApp) -> Path:
    """
    Save the project structure to a file

    Args:
        project_path: Root path of the project
        structure_content: Markdown content to save

    Returns:
        Path: Path to the saved file
    """
    try:
        # Create the output file
        output_file = app.psm.filebundler_dir / "project-structure.md"

        # Generate the structure content
        structure_content = _generate_project_structure(app)

        # Write the content
        output_file.write_text(structure_content, encoding="utf-8")

        logger.info(f"Project structure saved to {output_file}")
        return output_file

    except Exception as e:
        logger.error(f"Error saving project structure: {e}", exc_info=True)
        raise


def cli_entrypoint(argv: list[str] | None = None):
    """
    CLI entrypoint for generating and saving the project structure.
    Args:
        argv: List of command-line arguments (default: sys.argv)
    """
    if argv is None:
        argv = sys.argv
    try:
        assert len(argv) > 1, "Please provide the project path as an argument."
        filepath = Path(argv[1])
        # Optionally, validate path exists and is a directory
        # assert filepath.exists() and filepath.is_dir(), (
        #     f"Path {filepath} does not exist or is not a directory."
        # )
        app = FileBundlerApp(filepath)
        output_file = save_project_structure(app)
        print(f"[filebundler CLI] Project structure saved to: {output_file}")
        logging.info(f"Project structure saved to {output_file}")
    except Exception as e:
        print(f"[filebundler CLI] Error: {e}")
        logging.error(f"Error in project_structure CLI: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    cli_entrypoint()
