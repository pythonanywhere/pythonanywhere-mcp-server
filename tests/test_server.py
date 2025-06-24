import pytest

from pythonanywhere_mcp_server import server


@pytest.fixture()
def mock_FastMCP(mocker):
    """Mock the FastMCP class to avoid actual server creation."""
    return mocker.patch("pythonanywhere_mcp_server.server.FastMCP", autospec=True)


def test_create_server(monkeypatch, mock_FastMCP):
    monkeypatch.setenv("API_TOKEN", "dummy-token")
    server.create_server()
    mock_FastMCP.assert_called_once_with("PythonAnywhere Model Context Protocol Server")


@pytest.mark.parametrize(
    "register_fn", [
        "register_file_tools",
        "register_webapp_tools",
        "register_website_tools",
        "register_schedule_tools",
    ]
)
def test_register_tools(monkeypatch, mocker, mock_FastMCP, register_fn):
    monkeypatch.setenv("API_TOKEN", "dummy-token")
    mock_register = mocker.patch(
        f"pythonanywhere_mcp_server.server.{register_fn}" ,
        autospec=True
    )
    server.create_server()
    mock_register.assert_called_once_with(mock_FastMCP.return_value)


def test_missing_api_token(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    with pytest.raises(RuntimeError) as excinfo:
        server.create_server()
    assert "API_TOKEN environment variable must be set" in str(excinfo.value)
