from fastapi import HTTPException, status


class TeamNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена",
        )


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )


class TeamAccessDeniedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет доступа к этой команде",
        )


class TeamAdminRequiredError(HTTPException):
    def __init__(self, team_name: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Только админ команды {team_name} может выполнять это действие",
        )


class UserAlreadyInTeamError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"У пользователя {user_id} уже есть команда",
        )


class UserNotInTeamError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь не состоит в этой команде",
        )


class CannotRemoveTeamAdminError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить админа команды",
        )


class TeamCodeExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Код команды уже существует",
        )


class CannotAddTeamAdmin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Администратор команды может назначать только менажера и сотрудника",
        )
