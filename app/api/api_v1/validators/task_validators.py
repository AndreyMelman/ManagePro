from core.models import User, Task, TaskComment

from exceptions.task_exceptions import (
    TaskNotTeamError,
    TaskPermissionError,
    TaskCommentPermissionError,
    TaskCommentOwnerError,
)


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


def check_user_command(
    user: User,
    task: Task,
) -> None:
    if user.team_id != task.team_id:
        raise TaskCommentPermissionError()


def check_task_comment_owner(
    user: User,
    comment: TaskComment,
) -> None:
    if comment.user_id != user.id:
        raise TaskCommentOwnerError()
