from core.models import User, Task

from exceptions.task_exceptions import TaskNotTeamError, TaskPermissionError


def ensure_user_has_team(
    user: User,
) -> None:
    if not user.team_id:
        raise TaskNotTeamError()


def check_task_owner(
    user: User,
    task: Task,
) -> None:
    if task.creator_id != user.id:
        raise TaskPermissionError()
