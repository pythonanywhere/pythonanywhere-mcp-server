import pytest

import tools.website as website_tools


def test_list_websites(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.list.return_value = [
        {"domain": "test.com", "status": "running"}
    ]
    result = mcp.call_tool("list_websites", {})
    assert result == [{"domain": "test.com", "status": "running"}]


def test_list_websites_exception(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.list.side_effect = Exception("list error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("list_websites", {})
    assert "Failed to list websites: list error" in str(exc)


def test_create_website(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.create.return_value = {"domain": "test.com", "status": "created"}
    params = {"domain_name": "test.com", "command": "run.sh"}
    result = mcp.call_tool("create_website", params)
    assert result == {"domain": "test.com", "status": "created"}


def test_create_website_exception(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.create.side_effect = Exception("create error")
    params = {"domain_name": "test.com", "command": "run.sh"}
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("create_website", params)
    assert "Failed to create website: create error" in str(exc)


def test_delete_website(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.delete.return_value = True
    result = mcp.call_tool("delete_website", {"domain_name": "test.com"})
    mock_website.return_value.delete.assert_called_with("test.com")
    assert result is True


def test_delete_website_exception(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.delete.side_effect = Exception("delete error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("delete_website", {"domain_name": "test.com"})
    assert "Failed to delete website: delete error" in str(exc)


def test_reload_website(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    result = mcp.call_tool("reload_website", {"domain": "test.com"})
    mock_website.return_value.reload.assert_called_with("test.com")
    assert result == "Website 'test.com' reloaded."


def test_reload_website_auth_error(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    from pythonanywhere_core.base import AuthenticationError
    mock_website.return_value.reload.side_effect = AuthenticationError()
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("reload_website", {"domain": "test.com"})
    assert "Authentication failed" in str(exc)


def test_reload_website_other_error(mcp, mocker):
    website_tools.register_website_tools(mcp)
    mock_website = mocker.patch("tools.website.Website", autospec=True)
    mock_website.return_value.reload.side_effect = Exception("website reload error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("reload_website", {"domain": "test.com"})
    assert "website reload error" in str(exc)
