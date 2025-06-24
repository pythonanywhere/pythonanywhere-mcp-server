import pytest

import tools.schedule as schedule_tools

def test_list_scheduled_tasks(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.get_list.return_value = [
        {"id": 1, "command": "echo hi", "interval": "daily"}
    ]
    result = mcp.call_tool("list_scheduled_tasks", {})
    assert result == [{"id": 1, "command": "echo hi", "interval": "daily"}]


def test_list_scheduled_tasks_exception(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.get_list.side_effect = Exception("list error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("list_scheduled_tasks", {})
    assert "Failed to list scheduled tasks: list error" in str(exc)


def test_create_scheduled_task(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.create.return_value = {"id": 2, "command": "ls", "interval": "hourly"}
    params = {"command": "ls", "enabled": True, "interval": "hourly", "minute": 0}
    result = mcp.call_tool("create_scheduled_task", {"params": params})
    assert result == {"id": 2, "command": "ls", "interval": "hourly"}


def test_create_scheduled_task_exception(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.create.side_effect = Exception("create error")
    params = {"command": "ls", "enabled": True, "interval": "hourly", "minute": 0}
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("create_scheduled_task", {"params": params})
    assert "Failed to create scheduled task: create error" in str(exc)


def test_delete_scheduled_task(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.delete.return_value = True
    result = mcp.call_tool("delete_scheduled_task", {"task_id": 1})
    mock_schedule.return_value.delete.assert_called_with(1)
    assert result is True


def test_delete_scheduled_task_exception(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.delete.side_effect = Exception("delete error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("delete_scheduled_task", {"task_id": 1})
    assert "Failed to delete scheduled task: delete error" in str(exc)


def test_get_scheduled_task(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.get_specs.return_value = {"id": 1, "command": "ls"}
    result = mcp.call_tool("get_scheduled_task", {"task_id": 1})
    assert result == {"id": 1, "command": "ls"}


def test_get_scheduled_task_exception(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.get_specs.side_effect = Exception("get error")
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("get_scheduled_task", {"task_id": 1})
    assert "Failed to get scheduled task: get error" in str(exc)


def test_update_scheduled_task(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.update.return_value = {"id": 1, "command": "ls -l"}
    params = {"command": "ls -l"}
    result = mcp.call_tool("update_scheduled_task", {"task_id": 1, "params": params})
    assert result == {"id": 1, "command": "ls -l"}


def test_update_scheduled_task_exception(mcp, mocker):
    schedule_tools.register_schedule_tools(mcp)
    mock_schedule = mocker.patch("tools.schedule.Schedule", autospec=True)
    mock_schedule.return_value.update.side_effect = Exception("update error")
    params = {"command": "ls -l"}
    with pytest.raises(RuntimeError) as exc:
        mcp.call_tool("update_scheduled_task", {"task_id": 1, "params": params})
    assert "Failed to update scheduled task: update error" in str(exc)
