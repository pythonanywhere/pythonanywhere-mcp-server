# PythonAnywhere Model Context Protocol Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 
server acts as a bridge between AI-powered tools and your 
[PythonAnywhere](https://www.pythonanywhere.com/) account, enabling secure, 
programmatic management of files, websites, webapps, and scheduled tasks. By 
exposing a standardized interface, it allows language models and automation 
clients to perform operations—such as editing files, deploying web apps, or 
scheduling jobs -- on your behalf, all while maintaining fine-grained control
and auditability.

## Features
- **File management**: Read, upload, delete files and list directory trees. 
  _(also enables debugging with direct access to log files, which are just
  files on PythonAnywhere)_
- **ASGI Web app management**: Create, delete, reload, and list.
  _(as described in the [PythonAnywhere ASGI 
  documentation](https://help.pythonanywhere.com/pages/ASGICommandLine))_
- **WSGI Web app management**: Reload only _(at the moment)_.
- **Scheduled task management**: List, create, update, and delete.
  _(Note that this enables LLMs to execute arbitrary commands if a task is 
  scheduled to soon after creation and deleted after execution. For that we 
  would suggest running it with [mcp-server-time](https://pypi.org/project/mcp-server-time/)
  as models easily get confused about time.)_

## Installation
The MCP protocol is well-defined and supported by various clients, but 
installation is different depending on the client you are using. We will 
cover cases that we tried and tested.

In all cases, you need to have `uv` installed and available in your `PATH`.

Have your PythonAnywhere API token and username ready. You can find (or 
generate) your API token in the [API section of your PythonAnywhere 
account](https://www.pythonanywhere.com/account/#api_token).

### Desktop Extension - works with Claude Desktop
Probably the most straightforward way to install the MCP server is to use 
the [desktop extension](https://github.com/anthropics/dxt/) for Claude Desktop.

1. Open Claude Desktop.
2. **[Download the latest .dxt file](https://github.com/pythonanywhere/pythonanywhere-mcp-server/releases/latest/download/pythonanywhere-mcp-server.dxt)**.
3. Double-click on the downloaded .dxt file or drag the file into the window.
4. Configure your PythonAnywhere API token and username.
5. Restart Claude Desktop.

### Claude Code
Run:
   ```bash
   claude mcp add pythonanywhere-mcp-server \
   -e API_TOKEN=yourpythonanywhereapitoken \
   -e LOGNAME=yourpythonanywhereusername \
   -- uvx pythonanywhere-mcp-server
   ```

### GitHub Copilot in PyCharm:
Add it to your `mcp.json`.

```json
{
  "servers": {
    "pythonanywhere-mcp-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["pythonanywhere-mcp-server"],
      "env": {
        "API_TOKEN": "yourpythonanywhereapitoken",
        "LOGNAME": "yourpythonanywhereusername"
      }
    }
  }
}
```

### Claude Desktop (manual setup) and Cursor:
Add it to `claude_desktop_config.json` (for Claude Desktop) or (`mcp.json` 
for Cursor).

```json
{
  "mcpServers": {
    "pythonanywhere-mcp-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["pythonanywhere-mcp-server"],
      "env": {
        "API_TOKEN": "yourpythonanywhereapitoken",
        "LOGNAME": "yourpythonanywhereusername"
      }
    }
  }
}
```

## Caveats

Direct integration of an LLM with your PythonAnywhere account offers 
significant capabilities, but also introduces risks. We strongly advise 
maintaining human oversight, especially for sensitive actions such as 
modifying or deleting files.

If you are running multiple MCP servers simultaneously, be 
cautious -- particularly if any server can access external resources you do not
control, such as GitHub issues. These can become attack vectors. For more 
details, see [this story](https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/).

## Implementation

The server uses the [python mcp sdk](https://github.com/modelcontextprotocol/python-sdk) 
in connection with the [pythonanywhere-core](https://github.com/pythonanywhere/pythonanywhere-core) 
package ([docs](https://core.pythonanywhere.com/)), which wraps a subset of the [PythonAnywhere 
API](https://help.pythonanywhere.com/pages/API/) and may be expanded in 
the future as needed.
