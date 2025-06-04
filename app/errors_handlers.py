from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from exceptions.evaluation_exceptions import DuplicateEstimateError
from exceptions.team_exceptions import (
    TeamNotFoundError,
    TeamAccessDeniedError,
    TeamAdminRequiredError,
    CannotRemoveTeamAdminError,
    TeamCodeExistsError,
    CannotAddTeamAdminError,
    TeamAdminError,
    TaskCommentNotFoundError,
)
from exceptions.task_exceptions import (
    TaskNotTeamError,
    TaskNotFoundError,
    TaskPermissionError,
    InvalidAssigneeError,
    TaskCommentPermissionError,
    TaskCommentOwnerError,
)
from exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyInTeamError,
    UserNotInTeamError,
    UserCannotChangeRole,
)


def register_errors_handlers(main_app: FastAPI) -> None:

    @main_app.exception_handler(TeamNotFoundError)
    async def handle_team_not_found(
        request: Request,
        exc: TeamNotFoundError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Команда не найдена"},
        )

    @main_app.exception_handler(UserNotFoundError)
    async def handle_user_not_found(
        request: Request,
        exc: UserNotFoundError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"},
        )

    @main_app.exception_handler(TeamAccessDeniedError)
    async def handle_access_denied(
        request: Request,
        exc: TeamAccessDeniedError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "У вас нет доступа к этой команде"},
        )

    @main_app.exception_handler(TeamAdminRequiredError)
    async def handle_admin_required(
        request: Request,
        exc: TeamAdminRequiredError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": f"Только админ команды {exc.team_name} может выполнять это действие"
            },
        )

    @main_app.exception_handler(TeamAdminError)
    async def handle_admin_required(
        request: Request,
        exc: TeamAdminRequiredError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": f"Только админ без команды может выполнять это действие"
            },
        )

    @main_app.exception_handler(UserAlreadyInTeamError)
    async def handle_user_already_in_team(
        request: Request,
        exc: UserAlreadyInTeamError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"У пользователя {exc.user_id} уже есть команда"},
        )

    @main_app.exception_handler(UserNotInTeamError)
    async def handle_user_not_in_team(
        request: Request,
        exc: UserNotInTeamError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Пользователь не состоит в этой команде"},
        )

    @main_app.exception_handler(CannotRemoveTeamAdminError)
    async def handle_cannot_remove_admin(
        request: Request,
        exc: CannotRemoveTeamAdminError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Нельзя удалить админа команды"},
        )

    @main_app.exception_handler(TeamCodeExistsError)
    async def handle_code_exists(
        request: Request,
        exc: TeamCodeExistsError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Код команды уже существует"},
        )

    @main_app.exception_handler(CannotAddTeamAdminError)
    async def handle_cannot_add_admin(
        request: Request,
        exc: CannotAddTeamAdminError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Администратор может назначать только менеджера и сотрудника"
            },
        )

    @main_app.exception_handler(TaskNotTeamError)
    async def handle_task_not_found(
        request: Request,
        exc: TaskNotTeamError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "У пользователя нет команды"},
        )

    @main_app.exception_handler(UserCannotChangeRole)
    async def handle_user_cannot_change_role(
        request: Request,
        exc: UserCannotChangeRole,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Суперпользователь не может изменить свою роль"},
        )

    @main_app.exception_handler(TaskNotFoundError)
    async def handle_task_not_found(
        request: Request,
        exc: TaskNotFoundError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Задача не найдена"},
        )

    @main_app.exception_handler(TaskPermissionError)
    async def handle_task_permission_error(
        request: Request,
        exc: TaskPermissionError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Нет прав для обновления задачи другой команды"},
        )

    @main_app.exception_handler(InvalidAssigneeError)
    async def handle_invalid_assignee(
        request: Request,
        exc: InvalidAssigneeError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Исполнитель должен быть из той же команды, что и руководитель."
            },
        )

    @main_app.exception_handler(TaskCommentPermissionError)
    async def handle_task_comment_permission_error(
        request: Request,
        exc: TaskCommentPermissionError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Для просмотра комментариев задачи, необходимо быть в группе"
            },
        )

    @main_app.exception_handler(TaskCommentOwnerError)
    async def handle_task_comment_owner_error(
        request: Request,
        exc: TaskCommentOwnerError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Вы можете обновлять только свои комментарии"},
        )

    @main_app.exception_handler(TaskCommentNotFoundError)
    async def handle_task_comment_not_found_error(
        request: Request,
        exc: TaskCommentNotFoundError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Комментарий не найден"},
        )

    @main_app.exception_handler(DuplicateEstimateError)
    async def handle_duplicate_estimate_error(
        request: Request,
        exc: DuplicateEstimateError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "У задачи уже есть оценка"},
        )