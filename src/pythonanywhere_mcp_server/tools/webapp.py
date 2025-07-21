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
    def create_webapp(domain: str, python_version: str, virtualenv_path: str, project_path: str,
                      nuke: bool = False) -> str:
        """
        Create a new uWSGI-based web application for the given domain.

        This creates a new webapp on PythonAnywhere with the specified configuration.
        The webapp will be created using the specified Python version, virtual environment,
        and project path. If a webapp already exists for this domain, it will fail unless
        the nuke parameter is set to True.

        The WSGI configuration file can be found in /var/www. The file is of the format:
        domain.replace('.', '_') + '_wsgi.py'


        PythonAnywhere WSGI Configuration Guide for MCP Server

        This docstring provides comprehensive information about configuring WSGI files
        for various web application frameworks on PythonAnywhere hosting platform.

        Key Configurable Elements:


        1. Application Directory Path:
           The full path to your application directory
           path = '/home/{username}/{project_directory}'
           if path not in sys.path:
               sys.path.append(path)

        2. Application Import Statement:
           Import your WSGI application object
           from {main_app_file} import {app_object} as application

        Framework-Specific Templates:

        Flask Configuration:
           import sys

           # Update these paths
           path = '/home/{username}/{flask_app_directory}'
           if path not in sys.path:
               sys.path.append(path)

           # Update import to match your Flask app structure
           from {main_flask_file} import app as application

        Django Configuration:
           import os
           import sys

           # Update project path
           path = '/home/{username}/{django_project}'
           if path not in sys.path:
               sys.path.append(path)

           # Update Django settings module
           os.environ['DJANGO_SETTINGS_MODULE'] = '{project_name}.settings'

           from django.core.wsgi import get_wsgi_application
           application = get_wsgi_application()

        Custom WSGI Application:
           import sys

           path = '/home/{username}/{custom_app_directory}'
           if path not in sys.path:
               sys.path.append(path)

           from {custom_wsgi_file} import application

        Required Replacements for Any Framework:

        | Placeholder | Description | Example |
        |-------------|-------------|---------|
        | {username} | Your PythonAnywhere username | lcartwright20250703 |
        | {project_directory} | Your app's directory name | myflaskapp, mysite, api |
        | {main_app_file} | Main application file (no .py) | app, main, wsgi |
        | {app_object} | WSGI application object name | app, application, api |
        | {project_name} | Django project name | mysite, blog, shop |

        Universal WSGI Template:
           #!/usr/bin/python3

           import sys
           import os

           # REQUIRED: Update these variables for your application
           USERNAME = '{username}'
           PROJECT_DIR = '{project_directory}'
           MAIN_FILE = '{main_app_file}'
           APP_OBJECT = '{app_object}'

           # OPTIONAL: Django settings module (only for Django)
           # os.environ['DJANGO_SETTINGS_MODULE'] = '{project_name}.settings'

           # REQUIRED: Add your project directory to Python path
           path = f'/home/{USERNAME}/{PROJECT_DIR}'
           if path not in sys.path:
               sys.path.append(path)

           # REQUIRED: Import your WSGI application
           if MAIN_FILE and APP_OBJECT:
               exec(f'from {MAIN_FILE} import {APP_OBJECT} as application')
           else:
               # For Django
               from django.core.wsgi import get_wsgi_application
               application = get_wsgi_application()

        Key Requirements:

        1. Must define 'application' variable - This is the WSGI entry point
        2. Must add project path to sys.path - So Python can find your modules
        3. Must import your app correctly - Match your actual file/object names
        4. No development servers - Don't call app.run() or similar
        5. Executable permissions - Start with #!/usr/bin/python3

        Common Issues to Avoid:
        - Import errors: Ensure path is added to sys.path before importing
        - Wrong application object: Make sure you're importing the WSGI app, not a function
        - Development server calls: Remove any app.run() calls from your code
        - Hardcoded paths: Use the correct username and project paths
        - Missing dependencies: Ensure all required packages are installed

        Args:
            username (str): PythonAnywhere username for path construction
            project_directory (str): Directory name containing the web application
            main_app_file (str): Main application file name (without .py extension)
            app_object (str): Name of the WSGI application object to import
            project_name (str): Django project name (for Django apps only)

        Returns:
            str: Properly configured WSGI file content for PythonAnywhere deployment

        Example:
            For a Flask app:
                username = "myuser"
                project_directory = "myflaskapp"
                main_app_file = "app"
                app_object = "app"

            For a Django app:
                username = "myuser"
                project_directory = "mysite"
                project_name = "mysite"

        Note:
            Virtual environments should be configured in the PythonAnywhere web app
            setup tab, not in the WSGI file itself.


        Args:
            domain (str): The domain name for the new webapp (e.g., 'alice.pythonanywhere.com').
            python_version (str): Python version to use (e.g., '3.11', '3.10', '3.9').
            virtualenv_path (str): Path to the virtual environment to use.
            project_path (str): Path to the project directory containing the webapp code.
            nuke (bool, optional): If True, delete any existing webapp for this domain
                                 before creating the new one. Defaults to False.

        Returns:
            str: Status message indicating creation result.

        Raises:
            RuntimeError: If authentication fails, webapp already exists (and nuke=False),
                         or other API errors occur.
        """
        try:
            webapp = Webapp(domain)
            webapp.create(
                python_version=python_version,
                virtualenv_path=Path(virtualenv_path),
                project_path=Path(project_path),
                nuke=nuke
            )
            return f"Webapp '{domain}' created successfully with Python {python_version}."
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

        Returns:
            list: List of dictionaries containing webapp information.

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



