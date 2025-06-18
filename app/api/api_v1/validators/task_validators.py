from fastapi import (
    HTTPException,
    status,
)

from core.models import (
    User,
    Task,
    TaskComment,
)


def ensure_user_has_team(
    user: User,
) -> None:
    if not user.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "У пользователя нет команды"},
        )


def check_task_owner(
    user: User,
    task: Task,
) -> None:
    if task.creator_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "Нет прав для обновления задачи другой команды"},
        )


def check_user_command(
    user: User,
    task: Task,
) -> None:
    if user.team_id != task.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Для просмотра комментариев задачи, необходимо быть в группе"
            },
        )


def check_task_comment_owner(
    user: User,
    comment: TaskComment,
) -> None:
    if comment.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Вы можете обновлять только свои комментарии"},
        )
