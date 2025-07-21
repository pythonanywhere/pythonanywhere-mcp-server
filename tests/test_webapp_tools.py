import pytest

from pathlib import Path

import tools.webapp as webapp_tools

def test_reload_webapp(mcp, mocker):
    webapp_tools.register_webapp_tools(mcp)
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    result = mcp.call_tool("reload_webapp", {"domain": "test.com"})
    mock_webapp.assert_called_with("test.com")
    mock_webapp.return_value.reload.assert_called_once()
    assert result == "Webapp 'test.com' reloaded."


def test_reload_webapp_auth_error(mcp, mocker):
    webapp_tools.register_webapp_tools(mcp)
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    from pythonanywhere_core.base import AuthenticationError
    mock_webapp.return_value.reload.side_effect = AuthenticationError()
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("reload_webapp", {"domain": "test.com"})
    assert "Authentication failed" in str(exc)


def test_reload_webapp_other_error(mcp, mocker):
    webapp_tools.register_webapp_tools(mcp)
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    mock_webapp.return_value.reload.side_effect = Exception("webapp reload error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("reload_webapp", {"domain": "test.com"})
    assert "webapp reload error" in str(exc)


def test_create_webapp(mcp, mocker):
    webapp_domain = 'test.com'
    python_version = '3.10'
    virtualenv_path = Path('/test/venv/path')
    project_path = Path('/project/path')
    nuke = False

    webapp_tools.register_webapp_tools(mcp)
    mock_webapp = mocker.patch("tools.webapp.Webapp", autospec=True)
    result = mcp.call_tool(
        "create_webapp",
        {
            "domain": webapp_domain,
            "python_version": python_version,
            "virtualenv_path": virtualenv_path,
            "project_path": project_path,
            "nuke": nuke,
        }
    )
    mock_webapp.assert_called_with(webapp_domain)
    mock_webapp.return_value.create.assert_called_with(
        python_version=python_version,
        virtualenv_path=virtualenv_path,
        project_path=project_path,
        nuke=nuke
    )
    mock_webapp.return_value.create.assert_called_once()
    assert result == f"Webapp 'test.com' created successfully with Python {python_version}."

