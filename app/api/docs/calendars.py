from core.schemas.calendar import (
    CalendarMonthView,
    CalendarDayView,
)

CALENDAR_TAG = "Calendar"

GET_MONTH_VIEW = {
    "response_model": CalendarMonthView,
    "summary": "Получить календарь на месяц",
    "description": """
    Получить календарь команды на указанный месяц.

    - Требует прав доступа к команде
    - Возвращает все события команды за месяц
    - Включает встречи и задачи
    """,
    "responses": {
        200: {
            "description": "Успешное получение календаря",
            "content": {
                "application/json": {
                    "example": {
                        "year": 2024,
                        "month": 3,
                        "days": [
                            {
                                "date": "2024-03-01",
                                "meetings": [
                                    {
                                        "id": 1,
                                        "title": "Еженедельная встреча",
                                        "start_time": "10:00:00",
                                        "end_time": "11:00:00",
                                    }
                                ],
                                "tasks": [
                                    {
                                        "id": 1,
                                        "title": "Важная задача",
                                        "due_date": "2024-03-01",
                                    }
                                ],
                            }
                        ],
                    }
                }
            },
        },
        400: {"description": "Некорректные параметры даты"},
        403: {"description": "Нет прав для просмотра календаря"},
    },
}

GET_DAY_VIEW = {
    "response_model": CalendarDayView,
    "summary": "Получить календарь на день",
    "description": """
    Получить календарь команды на указанный день.

    - Требует прав доступа к команде
    - Возвращает все события команды за день
    - Включает встречи и задачи
    """,
    "responses": {
        200: {
            "description": "Успешное получение календаря",
            "content": {
                "application/json": {
                    "example": {
                        "date": "2024-03-20",
                        "meetings": [
                            {
                                "id": 1,
                                "title": "Еженедельная встреча",
                                "start_time": "10:00:00",
                                "end_time": "11:00:00",
                                "participants": [1, 2, 3],
                            }
                        ],
                        "tasks": [
                            {
                                "id": 1,
                                "title": "Важная задача",
                                "due_date": "2024-03-20",
                                "assignee_id": 1,
                            }
                        ],
                    }
                }
            },
        },
        400: {"description": "Некорректная дата"},
        403: {"description": "Нет прав для просмотра календаря"},
    },
}
