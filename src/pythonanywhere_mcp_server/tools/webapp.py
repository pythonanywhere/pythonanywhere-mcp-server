from pathlib import Path

from mcp.server.fastmcp import FastMCP

from pythonanywhere_core.webapp import Webapp
from pythonanywhere_core.base import AuthenticationError, NoTokenError

# ToDo: Add the log file functions once pythonanywhere-core webapp log file functions
# have been improved

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

    @mcp.tool()
    def create_webapp(domain: str, python_version: str, virtualenv_path: str, project_path: str) -> str:
        """
        Create a new uWSGI-based web application for the given domain.

        This creates a new webapp on PythonAnywhere with the specified configuration.
        The webapp will be created using the specified Python version, virtual environment,
        and project path. If a webapp already exists for this domain, it will fail unless
        the nuke parameter is set to True.

        The WSGI configuration file can be found in /var/www. The file is of the format:
        domain.replace('.', '_') + '_wsgi.py' It would be automatically created as side effect of running this tool.

        Note:
            Virtual environments should be configured in the PythonAnywhere web app
            configuration, not in the WSGI file itself.

        Args:
            domain (str): The domain name for the new webapp (e.g., 'alice.pythonanywhere.com').
            python_version (str): Python version to use (e.g., '3.11', '3.10', '3.9').
            virtualenv_path (str | None): Path to the virtual environment to use. (or None for
            no virtualenv when using one of pre-installed Pythons with batteries included packages)
            project_path (str): Path to the project directory containing the webapp code.

        Returns:
            str: Status message indicating creation result.

        Raises:
            RuntimeError: If authentication fails, webapp already exists (and nuke=False),
                         or other API errors occur. If 403 error is raised, it may mean that there
                         is already a non-uwsgi-based website. `list_websites` tool can be used to check that.
        """
        try:
            webapp = Webapp(domain)
            webapp.create(
                python_version=python_version,
                virtualenv_path=Path(virtualenv_path),
                project_path=Path(project_path),
                nuke=False
            )
            return f"Webapp '{domain}' created successfully."
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc

    @mcp.tool()
    def delete_webapp(domain: str) -> str:
        """
        Delete a uWSGI-based web application for the given domain.

        This permanently deletes the webapp configuration from PythonAnywhere. The actual
        files in your file system are not deleted, only the webapp configuration that
        serves them. This action cannot be undone.

        Args:
            domain (str): The domain name of the webapp to delete
                          (e.g., 'alice.pythonanywhere.com').

        Returns:
            str: Status message indicating deletion result.

        Raises:
            RuntimeError: If authentication fails, webapp doesn't exist, or other API errors occur.
        """
        try:
            Webapp(domain).delete()
            return f"Webapp '{domain}' deleted successfully."
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc

    @mcp.tool()
    def patch_webapp(domain: str, data: dict) -> dict:
        """
        Update configuration settings for a uWSGI-based web application.

        This allows you to modify various webapp settings such as the Python version,
        virtual environment path, source directory, and other configuration options.
        Only the fields provided in the data dictionary will be updated.

        In order for any changes to take effect you must reload the webapp.

        If you provide an invalid Python version you will receive a 400 error with an error
        message that the version you used is not a valid choice. You will need to choose a
        different Python version if you get this error.

        Args:
            domain (str): The domain name of the webapp to update
                          (e.g., 'alice.pythonanywhere.com').
            data (dict): Dictionary containing the configuration updates. Supported keys are:
                        - 'python_version': Python version (e.g., '3.11')
                        - 'virtualenv_path': Path to virtual environment
                        - 'source_directory': Path to source code directory
                        - 'working_directory': Working directory for the webapp
                        - 'force_https': Force the use of HTTPS when accessing the webapp
                        - 'password_protection_enabled': Enable basic HTTP password to your webapp, provided via PythonAnywhere not in the webapp code
                        - 'password_protection_username': The username used for HTTP password protection
                        - 'password_protection_password': The password used for HTTP password protection

        Returns:
            dict: Updated webapp configuration information.
                Example: {
                    "id": 2097234,
                    "user": username,
                    "domain_name": domain,
                    "python_version": "3.10",
                    "source_directory": f"/home/{username}/mysite",
                    "working_directory": f"/home/{username}/",
                    "virtualenv_path": "",
                    "expiry": "2025-10-16",
                    "force_https": False,
                    "password_protection_enabled": False,
                    "password_protection_username": "foo",
                    "password_protection_password": "bar"
                }

        Raises:
            RuntimeError: If authentication fails, webapp doesn't exist, or other API errors occur.
        """
        try:
            result = Webapp(domain).patch(data)
            return result
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc

    @mcp.tool()
    def list_webapps() -> list:
        """
        List all uWSGI-based web applications for the current user.

        This retrieves information about all webapps configured in your PythonAnywhere
        account. The returned list contains dictionaries with detailed information about
        each webapp including domain, Python version, paths, and status.

        On PythonAnywhere one may also have non-uWSGI-based websites (usually ASGI-based),
        which are not included in this list. For those, use the `list_websites` tool.

        Returns:
            list: List of dictionaries containing webapp information. Empty list means
            no WSGI-based webapps are deployed. That still could mean that there are
            non-WSGI-based apps that can be listed with the `list_websites` tool.

        See also:
            get_webapp_info: Get detailed information about a specific webapp.

        Raises:
            RuntimeError: If authentication fails or other API errors occur.
        """
        try:
            result = Webapp.list_webapps()
            return result
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc

    @mcp.tool()
    def get_webapp_info(domain: str) -> dict:
        """
        Get detailed information about a specific uWSGI-based web application.

        This retrieves comprehensive configuration and status information for the
        specified webapp, including paths, Python version, enabled status, and
        other configuration details.

        Args:
            domain (str): The domain name of the webapp to get information for
                          (e.g., 'alice.pythonanywhere.com').

        Returns:
            dict: Dictionary containing detailed webapp information including:
                  - "id": int,  # Unique identifier for the site or user session
                  - "user": str,  # Username associated with the deployment
                  - "domain_name": str,  # Domain name for the deployed site
                  - "python_version": str,  # Python version used, e.g., "3.10"
                  - "source_directory": str,  # Absolute path to the site's source directory
                  - "working_directory": str,  # Absolute path to the working directory
                  - "virtualenv_path": str,  # Path to the Python virtual environment (can be empty)
                  - "expiry": str,  # Expiration date in ISO format, e.g., "2025-10-16"
                  - "force_https": bool,  # Whether HTTPS is enforced
                  - "password_protection_enabled": bool,  # Whether password protection is enabled
                  - "password_protection_username": str,  # Username for password-protected access
                  - "password_protection_password": str   # Password for password-protected access


        Raises:
            RuntimeError: If authentication fails, webapp doesn't exist, or other API errors occur.
        """
        try:
            result = Webapp(domain).get()
            return result
        except (AuthenticationError, NoTokenError):
            raise RuntimeError("Authentication failed — check API_TOKEN and domain.")
        except Exception as exc:
            raise RuntimeError(str(exc)) from exc



