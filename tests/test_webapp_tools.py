import pytest
from pathlib import Path
from pythonanywhere_core.base import AuthenticationError

import tools.webapp as webapp_tools


@pytest.fixture
def setup_webapp_tools(mcp):
    webapp_tools.register_webapp_tools(mcp)
    return mcp


@pytest.mark.parametrize("tool_name,method_name,params,expected_params,expected_result", [
    ("reload_webapp", "reload", {"domain": "test.com"}, {}, "Webapp 'test.com' reloaded."),
    ("delete_webapp", "delete", {"domain": "test.com"}, {}, "Webapp 'test.com' deleted successfully."),
    ("get_webapp_info", "get", {"domain": "test.com"}, {}, {"domain_name": "test.com", "python_version": "3.10"}),
    ("patch_webapp", "patch", {"domain": "test.com", "data": {"python_version": "3.10"}}, {"python_version": "3.10"}, {"domain_name": "test.com", "python_version": "3.10"}),
])
def test_webapp_tools_success(setup_webapp_tools, mocker, tool_name, method_name, params, expected_params, expected_result):
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    
    if tool_name == "get_webapp_info" or tool_name == "patch_webapp":
        getattr(mock_webapp.return_value, method_name).return_value = expected_result
    
    result = setup_webapp_tools.call_tool(tool_name, params)
    
    if "domain" in params:
        mock_webapp.assert_called_with(params["domain"])
        if expected_params:
            getattr(mock_webapp.return_value, method_name).assert_called_with(expected_params)
        else:
            getattr(mock_webapp.return_value, method_name).assert_called_once()
    
    assert result == expected_result


@pytest.mark.parametrize("tool_name,method_name,params,side_effect,expected_error", [
    ("reload_webapp", "reload", {"domain": "test.com"}, AuthenticationError(), "Authentication failed"),
    ("reload_webapp", "reload", {"domain": "test.com"}, Exception("webapp reload error"), "webapp reload error"),
    ("delete_webapp", "delete", {"domain": "test.com"}, AuthenticationError(), "Authentication failed"),
    ("delete_webapp", "delete", {"domain": "test.com"}, Exception("delete error"), "delete error"),
    ("get_webapp_info", "get", {"domain": "test.com"}, AuthenticationError(), "Authentication failed"),
    ("get_webapp_info", "get", {"domain": "test.com"}, Exception("info error"), "info error"),
    ("patch_webapp", "patch", {"domain": "test.com", "data": {"python_version": "3.10"}}, AuthenticationError(), "Authentication failed"),
    ("patch_webapp", "patch", {"domain": "test.com", "data": {"python_version": "3.10"}}, Exception("patch error"), "patch error"),
])
def test_webapp_tools_errors(setup_webapp_tools, mocker, tool_name, method_name, params, side_effect, expected_error):
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    getattr(mock_webapp.return_value, method_name).side_effect = side_effect
    
    with pytest.raises(RuntimeError) as exc:
        setup_webapp_tools.call_tool(tool_name, params)
    assert expected_error in str(exc)


@pytest.mark.parametrize("side_effect,expected_error", [
    (AuthenticationError(), "Authentication failed"),
    (Exception("list error"), "list error"),
])
def test_list_webapps_errors(setup_webapp_tools, mocker, side_effect, expected_error):
    mocker.patch("tools.webapp.Webapp", autospec=True)
    mocker.patch("tools.webapp.Webapp.list_webapps", side_effect=side_effect)
    
    with pytest.raises(RuntimeError) as exc:
        setup_webapp_tools.call_tool("list_webapps", {})
    assert expected_error in str(exc)


def test_create_webapp(setup_webapp_tools, mocker):
    webapp_domain = 'test.com'
    python_version = '3.10'
    virtualenv_path = Path('/test/venv/path')
    project_path = Path('/project/path')

    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    result = setup_webapp_tools.call_tool(
        "create_webapp",
        {
            "domain": webapp_domain,
            "python_version": python_version,
            "virtualenv_path": virtualenv_path,
            "project_path": project_path,
        }
    )
    mock_webapp.assert_called_with(webapp_domain)
    mock_webapp.return_value.create.assert_called_with(
        python_version=python_version,
        virtualenv_path=virtualenv_path,
        project_path=project_path,
        nuke=False
    )
    mock_webapp.return_value.create.assert_called_once()
    assert result == f"Webapp 'test.com' created successfully."


@pytest.mark.parametrize("side_effect,expected_error", [
    (AuthenticationError(), "Authentication failed"),
    (Exception("webapp create error"), "webapp create error"),
])
def test_create_webapp_errors(setup_webapp_tools, mocker, side_effect, expected_error):
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    mock_webapp.return_value.create.side_effect = side_effect
    params = {
        "domain": "test.com",
        "python_version": "3.10",
        "virtualenv_path": "/test/venv/path",
        "project_path": "/project/path",
    }
    with pytest.raises(RuntimeError) as exc:
        setup_webapp_tools.call_tool("create_webapp", params)
    assert expected_error in str(exc)


def test_list_webapps(setup_webapp_tools, mocker):
    mocker.patch("tools.webapp.Webapp", autospec=True)
    expected = [{"domain_name": "test.com", "python_version": "3.10"}]
    mocker.patch("tools.webapp.Webapp.list_webapps", return_value=expected)
    result = setup_webapp_tools.call_tool("list_webapps", {})
    assert result == expected
