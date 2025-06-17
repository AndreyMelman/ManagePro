from fastapi import status

from core.schemas.evaluation import (
    EvaluationSchema,
    EvaluationBaseSchema,
)

EVALUATION_TAG = "Evaluations"

GET_EVALUATIONS = {
    "response_model": list[EvaluationBaseSchema],
    "summary": "Получить оценки",
    "description": """
    Получить список оценок пользователя.

    - Требует прав доступа
    - Возвращает список всех оценок пользователя
    """,
    "responses": {
        200: {
            "description": "Успешное получение оценок",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "score": 4.5,
                            "comment": "Хорошая работа",
                            "task_id": 1,
                            "created_at": "2024-03-20T10:00:00",
                        }
                    ]
                }
            },
        },
        403: {"description": "Нет прав для просмотра оценок"},
    },
}

GET_AVERAGE_SCORE = {
    "summary": "Получить среднюю оценку",
    "description": """
    Получить среднюю оценку пользователя за период.

    - Требует прав доступа
    - Можно указать период для расчета
    """,
    "responses": {
        200: {
            "description": "Успешное получение средней оценки",
            "content": {
                "application/json": {
                    "example": {
                        "average_score": 4.5,
                        "total_evaluations": 10,
                        "period": {
                            "start_date": "2024-01-01T00:00:00",
                            "end_date": "2024-03-20T23:59:59",
                        },
                    }
                }
            },
        },
        403: {"description": "Нет прав для просмотра оценок"},
    },
}

CREATE_EVALUATION = {
    "response_model": EvaluationSchema,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать оценку",
    "description": """
    Создать новую оценку для задачи.

    - Требует прав доступа к задаче
    - Оценка привязывается к конкретной задаче
    """,
    "responses": {
        201: {
            "description": "Оценка успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "score": 4.5,
                        "comment": "Отличная работа",
                        "task_id": 1,
                        "created_at": "2024-03-20T10:00:00",
                        "created_by": 1,
                    }
                }
            },
        },
        400: {"description": "Некорректные данные"},
        403: {"description": "Нет прав для создания оценки"},
        404: {"description": "Задача не найдена"},
    },
}
