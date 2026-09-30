import pytest

from mcp import Client

from pythonanywhere_mcp_server.server import create_server


EXPECTED_TOOLS = {
    "create_scheduled_task",
    "create_webapp",
    "create_website",
    "delete_path",
    "delete_scheduled_task",
    "delete_webapp",
    "delete_website",
    "get_scheduled_task",
    "get_webapp_info",
    "list_scheduled_tasks",
    "list_webapps",
    "list_websites",
    "patch_webapp",
    "read_file_or_directory",
    "reload_webapp",
    "reload_website",
    "tree",
    "update_scheduled_task",
    "upload_directory",
    "upload_text_file",
}


@pytest.fixture
def server(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "dummy-token")
    return create_server()


@pytest.mark.anyio
async def test_server_exposes_expected_tools(server):
    async with Client(server) as client:
        result = await client.list_tools()

    assert {tool.name for tool in result.tools} == EXPECTED_TOOLS


@pytest.mark.anyio
@pytest.mark.parametrize("tool_name,method_name,arguments", [
    ("get_webapp_info", "get", {"domain": "test.com"}),
    ("list_webapps", "list_webapps", {}),
    ("patch_webapp", "patch", {"domain": "test.com", "data": {"force_https": True}}),
])
async def test_webapp_password_is_absent_from_wire_result(
    server, mocker, tool_name, method_name, arguments
):
    config = {"domain_name": "test.com", "password_protection_password": "sentinel-secret"}
    mocker.patch(
        f"pythonanywhere_mcp_server.tools.webapp.Webapp.{method_name}",
        return_value=[config] if tool_name == "list_webapps" else config,
    )

    async with Client(server) as client:
        result = await client.call_tool(tool_name, arguments)

    assert not result.is_error
    serialised = result.model_dump_json()
    assert "test.com" in serialised
    assert "sentinel-secret" not in serialised
    assert "password_protection_password" not in serialised


@pytest.mark.anyio
async def test_api_failure_is_returned_as_actionable_tool_error(server, mocker):
    mocker.patch(
        "pythonanywhere_mcp_server.tools.schedule.Schedule.get_list",
        side_effect=Exception("list error"),
    )

    async with Client(server) as client:
        result = await client.call_tool("list_scheduled_tasks")

    assert result.is_error
    assert result.content[0].text == (
        "Error executing tool list_scheduled_tasks: "
        "Failed to list scheduled tasks: list error"
    )
