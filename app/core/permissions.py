from core.models import User, Task
from exceptions.task_exceptions import TaskNotTeamError, TaskPermissionError


def task_not_team_error(current_user: User) -> None:
    if not current_user.team_id:
        raise TaskNotTeamError()


def check_task_owner(current_user: User, task: Task) -> None:
    if task.creator_id != current_user.id:
        raise TaskPermissionError()
