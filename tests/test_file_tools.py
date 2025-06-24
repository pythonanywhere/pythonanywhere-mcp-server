import pytest

import tools.file as file_tools


def test_read_file_or_directory_file(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_get.return_value = b"file contents"
    result = mcp.call_tool("read_file_or_directory", {"path": "/some/file.txt"})
    assert result == "file contents"


def test_read_file_or_directory_directory(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_get.return_value = {"listing": ["a", "b"]}
    result = mcp.call_tool("read_file_or_directory", {"path": "/some/dir/"})
    assert result == str({"listing": ["a", "b"]})


def test_upload_text_file(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_post.return_value = 201
    result = mcp.call_tool("upload_text_file", {"dest_path": "/some/file.txt", "content": "hello"})
    assert result == "Uploaded to /some/file.txt (HTTP 201)."


def test_delete_path(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    result = mcp.call_tool("delete_path", {"path": "/some/file.txt"})
    mock_files.return_value.path_delete.assert_called_with("/some/file.txt")
    assert result == "Deleted /some/file.txt."


def test_read_file_or_directory_file_exception(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_get.side_effect = Exception("read error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("read_file_or_directory", {"path": "/some/file.txt"})
    assert "Failed to read file or directory: read error" in str(exc)


def test_upload_text_file_exception(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_post.side_effect = Exception("upload error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("upload_text_file", {"dest_path": "/some/file.txt", "content": "hello"})
    assert "Failed to upload text file: upload error" in str(exc)


def test_delete_path_exception(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.path_delete.side_effect = Exception("delete error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("delete_path", {"path": "/some/file.txt"})
    assert "Failed to delete path: delete error" in str(exc)


def test_directory_tree(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.tree_get.return_value = ["/a", "/b/c"]
    result = mcp.call_tool("tree", {"path": "/some/dir/"})
    assert result == ["/a", "/b/c"]


def test_directory_tree_exception(mcp, mocker):
    file_tools.register_file_tools(mcp)
    mock_files = mocker.patch("tools.file.Files", autospec=True)
    mock_files.return_value.tree_get.side_effect = Exception("tree error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("tree", {"path": "/some/dir/"})
    assert "Failed to get directory tree: tree error" in str(exc)
