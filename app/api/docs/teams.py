from fastapi import status

from core.schemas.team import TeamSchema

# Общие описания
TEAM_TAG = "Teams"
TEAM_PREFIX = "/teams"

# Документация для получения состава команды
GET_TEAM_WITH_USERS = {
    "response_model": list[TeamSchema],
    "summary": "Получить состав команды",
    "description": """
    Получить информацию о команде и её составе.

    - Требует прав доступа к команде
    - Возвращает команду со списком всех пользователей
    """,
    "responses": {
        200: {
            "description": "Успешное получение состава команды",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Команда разработки",
                        "code": "DEV",
                        "admin_id": 1,
                        "users": [
                            {"id": 1, "email": "admin@example.com", "role": "admin"},
                            {"id": 2, "email": "user@example.com", "role": "user"}
                        ]
                    }]
                }
            }
        },
        403: {"description": "Нет доступа к команде"},
        404: {"description": "Команда не найдена"}
    }
}

# Документация для создания команды
CREATE_TEAM = {
    "response_model": TeamSchema,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать новую команду",
    "description": """
    Создать новую команду.

    - Требует прав администратора
    - Создатель команды становится её администратором
    """,
    "responses": {
        201: {
            "description": "Команда успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Команда разработки",
                        "code": "DEV",
                        "admin_id": 1
                    }
                }
            }
        },
        400: {"description": "Некорректные данные или код команды уже существует"},
        403: {"description": "Нет прав для создания команды"}
    }
}

# Документация для добавления пользователя в команду
ADD_USER_TO_TEAM = {
    "status_code": status.HTTP_201_CREATED,
    "summary": "Добавить пользователя в команду",
    "description": """
    Добавить пользователя в команду.

    - Требует прав администратора команды
    - Пользователь не должен состоять в другой команде
    """,
    "responses": {
        201: {"description": "Пользователь успешно добавлен в команду"},
        400: {"description": "Пользователь уже состоит в команде"},
        403: {"description": "Нет прав для добавления пользователя"},
        404: {"description": "Команда или пользователь не найдены"}
    }
}

# Документация для удаления пользователя из команды
REMOVE_USER_FROM_TEAM = {
    "status_code": status.HTTP_204_NO_CONTENT,
    "summary": "Удалить пользователя из команды",
    "description": """
    Удалить пользователя из команды.

    - Требует прав администратора команды
    - Нельзя удалить администратора команды
    """,
    "responses": {
        204: {"description": "Пользователь успешно удален из команды"},
        400: {"description": "Нельзя удалить администратора команды"},
        403: {"description": "Нет прав для удаления пользователя"},
        404: {"description": "Команда или пользователь не найдены"}
    }
} 