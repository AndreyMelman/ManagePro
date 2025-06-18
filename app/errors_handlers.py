from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from exceptions.evaluation_exceptions import (
    DuplicateEstimateError,
)
from exceptions.role_exceptions import RoleError
from exceptions.team_exceptions import (
    TeamCodeExistsError,
)


def register_errors_handlers(main_app: FastAPI) -> None:

    @main_app.exception_handler(TeamCodeExistsError)
    async def handle_code_exists(
        request: Request,
        exc: TeamCodeExistsError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Код команды уже существует"},
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

    @main_app.exception_handler(RoleError)
    async def role_error_handler(
        request: Request,
        exc: RoleError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc),
                "error_type": "role_error",
                "role": exc.role,
                "user_id": exc.user_id,
            },
        )
