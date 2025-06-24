from pythonanywhere_core.files import Files
from typing import List

def register_tools(mcp):
    @mcp.tool(name="read_file_or_directory")
    def get_path(path: str) -> str:
        """
        Return the contents of a file or a directory listing.

        If the given path is a file, returns its contents as a string.
        If the path is a directory, returns a JSON string with its listing (recursively, up to 1000 entries).

        Args:
            path (str): The absolute path to the file or directory.

        Returns:
            str: File contents or JSON directory listing.
        """
        data = Files().path_get(path)
        if isinstance(data, (bytes, bytearray)):
            return data.decode()
        return str(data)

    @mcp.tool(name="upload_text_file")
    def upload_file(dest_path: str, content: str) -> str:
        """
        Create or replace a file with the given content (UTF-8 encoded).

        Args:
            dest_path (str): The absolute path where the file will be created or replaced.
            content (str): The text content to write to the file.

        Returns:
            str: Status message indicating upload result.
        """
        status = Files().path_post(dest_path, content.encode())
        return f"Uploaded to {dest_path} (HTTP {status})."

    @mcp.tool(name="delete_path")
    def delete_path(path: str) -> str:
        """
        Permanently delete a file or directory (recursively if directory).

        Args:
            path (str): The absolute path to the file or directory to delete.

        Returns:
            str: Status message indicating deletion result.
        """
        Files().path_delete(path)
        return f"Deleted {path}."

    @mcp.tool(name="directory_tree")
    def tree(path: str) -> List[str]:
        """
        Return a list of absolute paths contained in the given directory.

        Args:
            path (str): The absolute path to the directory.
                Home directory path is `/home/<username>/` where <username> is your username.

        Returns:
            List[str]: List of absolute paths contained in the directory.
        """
        listing = Files().tree_get(path)
        return listing
