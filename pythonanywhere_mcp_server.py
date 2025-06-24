import os

from mcp.server.fastmcp import FastMCP
from tools.file_tools import register_tools as register_file_tools
from tools.website_tools import register_tools as register_website_tools
from tools.schedule_tools import register_tools as register_schedule_tools

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise RuntimeError("API_TOKEN environment variable must be set.")

mcp = FastMCP("PythonAnywhere Model Context Protocol Server")

register_file_tools(mcp)
register_website_tools(mcp)
register_schedule_tools(mcp)

if __name__ == "__main__":
    mcp.run()
