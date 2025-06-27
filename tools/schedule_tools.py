from pythonanywhere_core.schedule import Schedule


def register_tools(mcp):
    @mcp.tool(name="list_scheduled_tasks")
    def list_scheduled_tasks() -> list[dict]:
        """
        List all scheduled tasks for the current user.  Empty list
        means that there are no scheduled tasks deployed.

        Returns:
            list[dict]: List of dictionaries, each representing a scheduled task.

        """
        try:
            return Schedule().get_list()
        except Exception as exc:
            raise RuntimeError(f"Failed to list scheduled tasks: {str(exc)}") from exc

    @mcp.tool(name="create_scheduled_task")
    def create_scheduled_task(params: dict) -> dict:
        """
        Create a new scheduled task.

        Args:
            params (dict): Dictionary with required scheduled task specs. Must include:
                - command (str): The command to run.
                - enabled (bool): Whether the task is enabled.
                - interval (str): 'daily' or 'hourly'.
                - hour (int, optional): Hour (24h format, for daily tasks).
                - minute (int): Minute.

        Returns:
            dict: Dictionary with created task specs.
        """
        try:
            return Schedule().create(params)
        except Exception as exc:
            raise RuntimeError(f"Failed to create scheduled task: {str(exc)}") from exc

    @mcp.tool(name="delete_scheduled_task")
    def delete_scheduled_task(task_id: int) -> bool:
        """
        Delete a scheduled task by its ID.

        Args:
            task_id (int): The ID of the scheduled task to delete.

        Returns:
            bool: True if deletion was successful.
        """
        try:
            return Schedule().delete(task_id)
        except Exception as exc:
            raise RuntimeError(f"Failed to delete scheduled task: {str(exc)}") from exc

    @mcp.tool(name="get_scheduled_task")
    def get_scheduled_task(task_id: int) -> dict:
        """
        Get the specifications of a scheduled task by its ID.

        Args:
            task_id (int): The ID of the scheduled task.

        Returns:
            dict: Dictionary of the task's specifications.
        """
        try:
            return Schedule().get_specs(task_id)
        except Exception as exc:
            raise RuntimeError(f"Failed to get scheduled task: {str(exc)}") from exc

    @mcp.tool(name="update_scheduled_task")
    def update_scheduled_task(task_id: int, params: dict) -> dict:
        """
        Update an existing scheduled task.

        Args:
            task_id (int): The ID of the scheduled task to update.
            params (dict): Dictionary of specs to update. Should include at least one of:
                - command, enabled, interval, hour, minute.

        Returns:
            dict: Dictionary with updated task specs.
        """
        try:
            return Schedule().update(task_id, params)
        except Exception as exc:
            raise RuntimeError(f"Failed to update scheduled task: {str(exc)}") from exc
