from fastapi import status

from core.schemas.task import TaskSchema

TASK_TAG = "Tasks"

GET_TASK = {
    "response_model": TaskSchema,
    "summary": "Получить задачу",
    "description": """
    Получить задачу по ID.

    - Требует прав доступа к задаче
    - Возвращает информацию о задаче
    """,
    "responses": {
        200: {
            "description": "Успешное получение задачи",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Разработка нового функционала",
                        "description": "Необходимо реализовать новый функционал",
                        "status": "in_progress",
                        "assignee_id": 1,
                        "created_by": 1,
                    }
                }
            },
        },
        403: {"description": "Нет доступа к задаче"},
        404: {"description": "Задача не найдена"},
    },
}

CREATE_TASK = {
    "response_model": TaskSchema,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать новую задачу",
    "description": """
    Создать новую задачу.

    - Требует прав пользователя
    - Создатель задачи становится её ответственным
    """,
    "responses": {
        201: {
            "description": "Задача успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Разработка нового функционала",
                        "description": "Необходимо реализовать новый функционал",
                        "status": "new",
                        "assignee_id": 1,
                        "created_by": 1,
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        403: {"description": "Нет прав для создания задачи"},
    },
}

UPDATE_TASK = {
    "response_model": TaskSchema,
    "summary": "Обновить задачу",
    "description": """
    Обновить существующую задачу.

    - Требует прав доступа к задаче
    - Можно обновить только доступные поля
    """,
    "responses": {
        200: {
            "description": "Задача успешно обновлена",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Обновленная задача",
                        "description": "Обновленное описание",
                        "status": "in_progress",
                        "assignee_id": 1,
                        "created_by": 1,
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        403: {"description": "Нет прав для обновления задачи"},
        404: {"description": "Задача не найдена"},
    },
}

DELETE_TASK = {
    "status_code": status.HTTP_204_NO_CONTENT,
    "summary": "Удалить задачу",
    "description": """
    Удалить существующую задачу.

    - Требует прав доступа к задаче
    - Задача будет полностью удалена из системы
    """,
    "responses": {
        204: {"description": "Задача успешно удалена"},
        403: {"description": "Нет прав для удаления задачи"},
        404: {"description": "Задача не найдена"},
    },
}
