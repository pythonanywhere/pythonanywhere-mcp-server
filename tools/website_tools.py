from pythonanywhere_core.website import Website
from pythonanywhere_core.webapp import Webapp
from pythonanywhere_core.base import AuthenticationError, NoTokenError
from typing import List, Any


def register_tools(mcp):
    @mcp.tool(name="reload_webapp")
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

    @mcp.tool(name="reload_website")
    def reload_website(domain: str) -> str:
        """
        Reload an ASGI-based website for the given domain.

        This is for ASGI-based web applications on PythonAnywhere. For uWSGI-based
        web applications, use the `reload_webapp` tool instead. Any changes to the
        code require a reload to take effect.

        Args:
            domain (str): The domain name of the website to reload
                          (e.g., 'alice.pythonanywhere.com').

        Returns:
            str: Status message indicating reload result.
        """
        try:
            Website().reload(domain)
            return f"Website '{domain}' reloaded."
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc

    @mcp.tool(name="list_websites")
    def list_websites() -> List[dict[str, Any]]:
        """
        Return info dictionaries for every ASGI website configured for the current
        user.  Empty list means that there are no websites deployed.

        Returns:
            List[dict[str, Any]]: List of dictionaries with website information.

        """
        try:
            return Website().list()
        except Exception as exc:
            raise RuntimeError(f"Failed to list websites: {str(exc)}") from exc

    @mcp.tool(name="create_website")
    def create_website(domain_name: str, command: str) -> dict:
        """
        Create a new website with the specified domain name and command.

        This function is primarily used to create a new ASGI-based website on
        PythonAnywhere, but it can also be used for any website that communicates via
        a Unix domain socket. The provided command must use the `DOMAIN_SOCKET`
        environment variable to bind to the socket.

        Args:
            domain_name (str): The domain name for the new website
                               (e.g., `yourusername.pythonanywhere.com` or `www.mydomain.com`).
            command (str): The command to run for the new website. Examples:
                - For FastAPI (ASGI):
                    `/usr/local/bin/uvicorn myapp:app \
                         --app-dir '/home/yourusername/fastapi/' \
                         --uds ${DOMAIN_SOCKET}`
                - For async Django:
                    `/home/yourusername/.virtualenvs/my_venv/bin/uvicorn asyncdjango.asgi:application \
                         --app-dir /home/yourusername/asyncdjango \
                         --uds ${DOMAIN_SOCKET} `
                - For non-ASGI websites (e.g., Streamlit):
                    `/home/yourusername/.virtualenvs/my_venv/bin/streamlit \
                         run /home/yourusername/my_streamlit/streamlit_app.py \
                         --server.address "unix://${DOMAIN_SOCKET}" \
                         --server.enableCORS false \
                         --server.enableXsrfProtection false \
                         --server.enableWebsocketCompression false`

        Returns:
            dict: A dictionary containing information about the created website.
        """
        try:
            return Website().create(domain_name, command)
        except Exception as exc:
            raise RuntimeError(f"Failed to create website: {str(exc)}") from exc

    @mcp.tool(name="delete_website")
    def delete_website(domain_name: str) -> dict:
        """
        Delete a website with the given domain name.

        Args:
            domain_name (str): The domain name for the website to delete.

        Returns:
            dict: Empty dictionary on success.
        """
        try:
            return Website().delete(domain_name)
        except Exception as exc:
            raise RuntimeError(f"Failed to delete website: {str(exc)}") from exc
