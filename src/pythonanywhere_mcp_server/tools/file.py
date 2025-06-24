from mcp.server.fastmcp import FastMCP

from pythonanywhere_core.files import Files


def register_file_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def read_file_or_directory(path: str) -> str:
        """
        Return the contents of a file or a directory listing.

        If the given path is a file, returns its contents as a string.
        If the path is a directory, returns a JSON string with its listing (recursively, up to 1000 entries).

        Args:
            path (str): The absolute path to the file or directory.

        Returns:
            str: File contents or JSON directory listing.
        """
        try:
            data = Files().path_get(path)
            if isinstance(data, (bytes, bytearray)):
                return data.decode()
            return str(data)
        except Exception as exc:
            raise RuntimeError(f"Failed to read file or directory: {str(exc)}") from exc

    @mcp.tool()
    def upload_text_file(dest_path: str, content: str) -> str:
        """
        Create or replace a file with the given content (UTF-8 encoded).

        Args:
            dest_path (str): The absolute path where the file will be created or replaced.
            content (str): The text content to write to the file.

        Returns:
            str: Status message indicating upload result.
        """
        try:
            status = Files().path_post(dest_path, content.encode())
            return f"Uploaded to {dest_path} (HTTP {status})."
        except Exception as exc:
            raise RuntimeError(f"Failed to upload text file: {str(exc)}") from exc

    @mcp.tool()
    def delete_path(path: str) -> str:
        """
        Permanently delete a file or directory (recursively if directory).

        Args:
            path (str): The absolute path to the file or directory to delete.

        Returns:
            str: Status message indicating deletion result.
        """
        try:
            Files().path_delete(path)
            return f"Deleted {path}."
        except Exception as exc:
            raise RuntimeError(f"Failed to delete path: {str(exc)}") from exc

    @mcp.tool()
    def tree(path: str) -> list[str]:
        """
        Return a list of absolute paths contained in the given directory.

        Args:
            path (str): The absolute path to the directory.
                Home directory path is `/home/<username>/` where <username> is your username.

        Returns:
            List[str]: List of absolute paths contained in the directory.
        """
        try:
            listing = Files().tree_get(path)
            return listing
        except Exception as exc:
            raise RuntimeError(f"Failed to get directory tree: {str(exc)}") from exc
