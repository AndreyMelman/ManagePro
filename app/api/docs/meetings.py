from fastapi import status

from core.schemas.meeting import MeetingSchema

MEETING_TAG = "Meetings"

GET_USER_MEETINGS = {
    "response_model": list[MeetingSchema],
    "summary": "Получить встречи пользователя",
    "description": """
    Получить список встреч пользователя.

    - Требует прав менеджера
    - Возвращает список встреч с пагинацией
    - Можно включить отмененные встречи
    """,
    "responses": {
        200: {
            "description": "Успешное получение встреч",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "Еженедельная встреча",
                            "description": "Обсуждение текущих задач",
                            "start_time": "2024-03-20T10:00:00",
                            "end_time": "2024-03-20T11:00:00",
                            "participants": [1, 2, 3],
                            "created_by": 1,
                            "status": "scheduled",
                        }
                    ]
                }
            },
        },
        403: {"description": "Нет прав для просмотра встреч"},
    },
}

GET_MEETING = {
    "response_model": MeetingSchema,
    "summary": "Получить встречу",
    "description": """
    Получить информацию о конкретной встрече.

    - Требует прав доступа к встрече
    - Возвращает детальную информацию о встрече
    """,
    "responses": {
        200: {
            "description": "Успешное получение встречи",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Еженедельная встреча",
                        "description": "Обсуждение текущих задач",
                        "start_time": "2024-03-20T10:00:00",
                        "end_time": "2024-03-20T11:00:00",
                        "participants": [1, 2, 3],
                        "created_by": 1,
                        "status": "scheduled",
                    }
                }
            },
        },
        403: {"description": "Нет доступа к встрече"},
        404: {"description": "Встреча не найдена"},
    },
}

CREATE_MEETING = {
    "response_model": MeetingSchema,
    "status_code": status.HTTP_201_CREATED,
    "summary": "Создать встречу",
    "description": """
    Создать новую встречу.

    - Требует прав менеджера
    - Проверяет доступность времени для всех участников
    - Участники должны быть из той же команды
    """,
    "responses": {
        201: {
            "description": "Встреча успешно создана",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Новая встреча",
                        "description": "Описание встречи",
                        "start_time": "2024-03-20T10:00:00",
                        "end_time": "2024-03-20T11:00:00",
                        "participants": [1, 2, 3],
                        "created_by": 1,
                        "status": "scheduled",
                    }
                }
            },
        },
        400: {"description": "Некорректные данные или конфликт времени"},
        403: {"description": "Нет прав для создания встречи"},
    },
}

UPDATE_MEETING = {
    "response_model": MeetingSchema,
    "summary": "Обновить встречу",
    "description": """
    Обновить существующую встречу.

    - Требует прав менеджера
    - Проверяет доступность нового времени
    - Участники должны быть из той же команды
    """,
    "responses": {
        200: {
            "description": "Встреча успешно обновлена",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Обновленная встреча",
                        "description": "Новое описание",
                        "start_time": "2024-03-20T14:00:00",
                        "end_time": "2024-03-20T15:00:00",
                        "participants": [1, 2, 3],
                        "created_by": 1,
                        "status": "scheduled",
                    }
                }
            },
        },
        400: {"description": "Некорректные данные или конфликт времени"},
        403: {"description": "Нет прав для обновления встречи"},
        404: {"description": "Встреча не найдена"},
    },
}

CANCEL_MEETING = {
    "response_model": MeetingSchema,
    "summary": "Отменить встречу",
    "description": """
    Отменить существующую встречу.

    - Требует прав менеджера
    - Встреча должна быть в будущем
    """,
    "responses": {
        200: {
            "description": "Встреча успешно отменена",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Отмененная встреча",
                        "description": "Описание встречи",
                        "start_time": "2024-03-20T10:00:00",
                        "end_time": "2024-03-20T11:00:00",
                        "participants": [1, 2, 3],
                        "created_by": 1,
                        "status": "cancelled",
                    }
                }
            },
        },
        403: {"description": "Нет прав для отмены встречи"},
        404: {"description": "Встреча не найдена"},
    },
}
