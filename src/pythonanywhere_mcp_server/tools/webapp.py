from mcp.server.fastmcp import FastMCP

from pythonanywhere_core.webapp import Webapp
from pythonanywhere_core.base import AuthenticationError, NoTokenError


def register_webapp_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def reload_webapp(domain: str) -> str:
        """
        Reload a uWSGI-based web application for the given domain.

        This reloads uwsgi-based web applications on PythonAnywhere. For ASGI-based
        web applications, use the `reload_website` tool instead. Any changes to the
        code require a reload to take effect.

        Args:
            domain (str): The domain name of the web application to reload
                          (e.g., 'alice.pythonanywhere.com').

        Returns:
            str: Status message indicating reload's result.
        """
        try:
            Webapp(domain).reload()
            return f"Webapp '{domain}' reloaded."
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc
