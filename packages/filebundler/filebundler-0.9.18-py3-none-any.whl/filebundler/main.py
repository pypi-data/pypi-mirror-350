# filebundler/main.py
import os
import sys
import atexit
import logging
import argparse

from filebundler import app
from filebundler._version import VERSION


def main():
    """Entry point function for the package."""

    # Register app.cleanup to be called on normal exit
    atexit.register(app.cleanup)

    # priniting anything to stdout will break the MCP server
    # print(f"Running FileBundler version {VERSION}")

    parser = argparse.ArgumentParser(description="File Bundler App")
    parser.add_argument(
        "-v",
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="Show program's version number and exit",
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Subcommands: web (default), cli"
    )

    # Web (default) subcommand
    parser_web = subparsers.add_parser(
        "web", help="Launch the FileBundler web app (default)"
    )
    parser_web.add_argument(
        "--headless", action="store_true", help="Run in headless mode"
    )
    parser_web.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)",
    )
    parser_web.add_argument(
        "--theme",
        default="dark",
        choices=["light", "dark"],
        help="Set the Streamlit theme (light or dark)",
    )

    # CLI subcommand
    parser_cli = subparsers.add_parser(
        "cli", help="Run CLI actions without starting the web server"
    )
    parser_cli.add_argument(
        "action", choices=["tree", "chat_instruction", "unbundle"], help="CLI action to perform ('tree', 'chat_instruction', 'unbundle')"
    )
    parser_cli.add_argument(
        "project_path",
        nargs="?",
        default=os.getcwd(),
        help="Path to the project root (default: current directory)",
    )
    parser_cli.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)",
    )

    # MCP Server subcommand
    parser_mcp = subparsers.add_parser("mcp", help="Start the FileBundler MCP server")
    parser_mcp.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level (default: info)",
    )

    # If no subcommand is provided, default to '--version'
    if len(sys.argv) == 1 or (
        len(sys.argv) > 1 and sys.argv[1] not in ["web", "cli", "mcp"]
    ):
        print("No command provided, defaulting to '--version'")
        sys.argv.insert(1, "--version")

    args = parser.parse_args()

    # Set log level
    if hasattr(args, "log_level") and args.log_level:
        os.environ["LOG_LEVEL"] = args.log_level

    if args.command == "cli":
        # CLI mode
        if args.action == "tree":
            from filebundler.services.project_structure import cli_entrypoint
            cli_entrypoint([sys.argv[0], args.project_path])
            return
        elif args.action == "chat_instruction":
            from filebundler.services.cli_chat_instruction import cli_chat_instruction
            cli_chat_instruction()
            return
        elif args.action == "unbundle":
            from filebundler.services.cli_unbundle import cli_unbundle
            cli_unbundle()
            return
        else:
            import logging
            logger = logging.getLogger("filebundler.cli")
            logger.error(f"Unknown CLI action: {args.action}")
            print(f"Unknown CLI action: {args.action}")
            sys.exit(1)
    elif args.command == "mcp":
        # MCP Server mode
        from filebundler.mcp_server import main as mcp_main
        # import asyncio
        # asyncio.run(mcp_main())

        mcp_main()
        return

    # Web mode (default)
    if "ANTHROPIC_API_KEY" not in os.environ and "GEMINI_API_KEY" not in os.environ:
        logging.warning(
            "\033[93mAnthropic or Gemini API key not found in environment variables. "
            "Some features may not work as expected. "
            "(Color might not be supported in all terminals)\033[0m"
        )

    # When called as an installed package, we need to run Streamlit with this file
    import streamlit.web.cli as stcli

    # Get the absolute path to this file
    current_file = os.path.abspath(__file__)

    try:
        # Set up Streamlit arguments to run this file
        st_args = ["streamlit", "run", current_file, "--global.developmentMode=false"]
        if hasattr(args, "headless") and args.headless:
            st_args.append("--server.headless=true")
        if hasattr(args, "theme") and args.theme:
            st_args.append(f"--theme.base={args.theme}")

        sys.argv = st_args

        # Run Streamlit CLI with this file
        sys.exit(stcli.main())  # type: ignore
    except KeyboardInterrupt:
        # Handle Ctrl+C at the top level
        logging.info("Keyboard interrupt received, exiting...")
        app.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    atexit.register(app.cleanup)

    try:
        app.main()
    except KeyboardInterrupt:
        sys.exit(0)
