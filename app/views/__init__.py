from fastapi import APIRouter, Request

from utils.templates import templates

from .auth.views import router as auth_router
from .teams.views import router as teams_router
from .tasks.views import router as tasks_router
from .task_comments.views import router as task_comments_router
from .meetings.views import router as meetings_router
from .evaluations.views import router as evaluations_router

router = APIRouter()


@router.get("/", name="home")
def index_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


router.include_router(auth_router)
router.include_router(teams_router)
router.include_router(tasks_router)
router.include_router(task_comments_router)
router.include_router(meetings_router)
router.include_router(evaluations_router)
