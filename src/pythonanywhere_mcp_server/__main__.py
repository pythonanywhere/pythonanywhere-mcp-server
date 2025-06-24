"""Entry point for the PythonAnywhere MCP server."""

import sys
from .server import create_server

def main():
    """Main entry point for the MCP server."""
    try:
        mcp = create_server()
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()