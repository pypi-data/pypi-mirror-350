from typing import List
from pathlib import Path

from filebundler.models.FileItem import FileItem
from filebundler.models.Bundle import Bundle

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("filebundler")


@mcp.tool()
def export_file_bundle(
    file_paths: List[str], project_path: str, bundle_name: str = "mcp-bundle"
) -> str:
    """
    Bundles the specified files from a project and returns their content in XML format.

    Args:
        file_paths: A list of relative file paths (strings) to include in the bundle.
        project_path: The absolute path to the root of the project.
        bundle_name: An optional name for the bundle (string).

    Returns:
        An XML string containing the bundled file contents.
    """
    try:
        proj_path = Path(project_path)
        if not proj_path.is_dir():
            return f"<error>Project path '{project_path}' does not exist or is not a directory.</error>"

        file_items: List[FileItem] = []
        for rel_path_str in file_paths:
            # FileItem expects path relative to project_path for initialization,
            # but its internal path becomes absolute after validation.
            # Here, we are creating FileItem with the relative path string.
            # The project_path argument to FileItem constructor helps it resolve the full path.
            file_item = FileItem(
                path=Path(rel_path_str),
                project_path=proj_path,
                parent=None,
                children=[],
                selected=False,
            )
            if file_item.path.exists() and not file_item.is_dir:
                file_items.append(file_item)
            elif not file_item.path.exists():
                # Consider how to report missing files; for now, they are silently skipped by Bundle
                # Or we can return an error/warning message part
                pass  # Silently skip missing files for now, Bundle will also filter them

        if not file_items:
            return "<error>No valid files found to bundle. All specified paths might be directories, non-existent, or the list was empty.</error>"

        bundle = Bundle(name=bundle_name, file_items=file_items)
        return bundle.export_code()
    except Exception as e:
        # Log the exception e for server-side diagnostics
        return f"<error>An unexpected error occurred: {str(e)}</error>"


# async def main():
# """Runs the MCP server."""
# from mcp.server.stdio import stdio_server
# async with stdio_server():
#     # async with stdio_server() as (read_stream, write_stream):
#     mcp.run()
def main():
    mcp.run()


# Run the MCP server locally
if __name__ == "__main__":
    # import asyncio
    # asyncio.run(main())
    main()
