from fastapi import status

from core.schemas.task_comment import TaskCommentSchema

TASK_COMMENT_TAG = "Task Comments"

GET_TASK_COMMENTS = {
    "response_model": list[TaskCommentSchema],
    "summary": "Получить комментарии к задаче",
    "description": """
    Получить все комментарии к конкретной задаче.

    - Требует прав доступа к задаче
    - Возвращает список комментариев
    """,
    "responses": {
        200: {
            "description": "Успешное получение комментариев",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "content": "Комментарий к задаче",
                            "created_at": "2024-03-20T10:00:00",
                            "user_id": 1,
                            "task_id": 1,
                        }
                    ]
                }
            },
        },
        403: {"description": "Нет доступа к задаче"},
        404: {"description": "Задача не найдена"},
    },
}

CREATE_TASK_COMMENT = {
    "response_model": TaskCommentSchema,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать комментарий к задаче",
    "description": """
    Создать новый комментарий к задаче.

    - Требует прав доступа к задаче
    - Комментарий привязывается к текущему пользователю
    """,
    "responses": {
        201: {
            "description": "Комментарий успешно создан",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "content": "Новый комментарий",
                        "created_at": "2024-03-20T10:00:00",
                        "user_id": 1,
                        "task_id": 1,
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        403: {"description": "Нет прав для создания комментария"},
        404: {"description": "Задача не найдена"},
    },
}

UPDATE_TASK_COMMENT = {
    "response_model": TaskCommentSchema,
    "summary": "Обновить комментарий",
    "description": """
    Обновить существующий комментарий.

    - Требует прав доступа к комментарию
    - Можно обновить только свои комментарии
    """,
    "responses": {
        200: {
            "description": "Комментарий успешно обновлен",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "content": "Обновленный комментарий",
                        "created_at": "2024-03-20T10:00:00",
                        "user_id": 1,
                        "task_id": 1,
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        403: {"description": "Нет прав для обновления комментария"},
        404: {"description": "Комментарий не найден"},
    },
}

DELETE_TASK_COMMENT = {
    "status_code": status.HTTP_204_NO_CONTENT,
    "summary": "Удалить комментарий",
    "description": """
    Удалить существующий комментарий.

    - Требует прав доступа к комментарию
    - Можно удалить только свои комментарии
    """,
    "responses": {
        204: {"description": "Комментарий успешно удален"},
        403: {"description": "Нет прав для удаления комментария"},
        404: {"description": "Комментарий не найден"},
    },
}
