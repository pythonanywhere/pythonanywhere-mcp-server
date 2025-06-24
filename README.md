# PythonAnywhere Model Context Protocol Server

Provides a modular server for managing files, websites, webapps, and 
scheduled tasks on PythonAnywhere using the Model Context Protocol (MCP).

## Features
- **File management**: Read, upload, delete files and list directory trees.
- **Website & webapp management**: Create, delete, reload, and list ASGI/WSGI websites and webapps.
- **Scheduled task management**: List, create, update, and delete scheduled tasks.

## Usage
Example configuration of a server:

For GitHub Copilot:

```json
{
  "servers": {
    "pythonanywhere-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory", 
        "/path/to/pythonanywhere-mcp-server", 
        "run", 
        "pythonanywhere_mcp_server.py"
      ],
      "env": {
        "API_TOKEN": "yourpythonanywhereapitoken",
        "LOGNAME": "yourpythonanywhereusername"
      }
    }
  }
}
```

For Claude Desktop:

```json
{
  "mcpServers": {
    "pythonanywhere-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory", 
        "/path/to/pythonanywhere-mcp-server", 
        "run", 
        "pythonanywhere_mcp_server.py"
      ],
      "env": {
        "API_TOKEN": "yourpythonanywhereapitoken",
        "LOGNAME": "yourpythonanywhereusername"
      }
    }
  }
}
```


## License
MIT
