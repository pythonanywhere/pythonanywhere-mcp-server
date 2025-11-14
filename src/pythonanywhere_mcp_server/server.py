import os

from mcp.server.fastmcp import FastMCP
from . import __version__
from .tools.file import register_file_tools
from .tools.webapp import register_webapp_tools
from .tools.website import register_website_tools
from .tools.schedule import register_schedule_tools


def create_server():
    """Create the MCP server."""
    # Set client identifier for API analytics
    os.environ["PYTHONANYWHERE_CLIENT"] = f"mcp-server/{__version__}"

    API_TOKEN = os.getenv("API_TOKEN")
    if not API_TOKEN:
        raise RuntimeError("API_TOKEN environment variable must be set.")

    mcp = FastMCP("PythonAnywhere Model Context Protocol Server")

    register_file_tools(mcp)
    register_website_tools(mcp)
    register_schedule_tools(mcp)
    register_webapp_tools(mcp)

    return mcp