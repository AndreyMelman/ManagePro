from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer

from core.config import settings

from .auth import router as auth_router
from .users import router as users_router
from .teams import router as teams_router
from .tasks import router as tasks_router
from .task_comments import router as task_comments_router
from .evaluations import router as evaluations_router
from .meetings import router as meetings_router
from .calendars import router as calendars_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(teams_router, prefix=settings.api.v1.teams)
router.include_router(tasks_router, prefix=settings.api.v1.tasks)
router.include_router(task_comments_router, prefix=settings.api.v1.task_comments)
router.include_router(evaluations_router, prefix=settings.api.v1.evaluation)
router.include_router(meetings_router, prefix=settings.api.v1.meeting)
router.include_router(calendars_router, prefix=settings.api.v1.calendar)