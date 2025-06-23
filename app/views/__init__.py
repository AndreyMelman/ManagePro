from fastapi import APIRouter, Request

from utils.templates import templates

router = APIRouter()


@router.get("/", name="home")
def index_page(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


def include_routers():
    from .auth.views import router as auth_router
    from .teams.views import router as teams_router
    from .tasks.views import router as tasks_router
    from .task_comments.views import router as task_comments_router

    router.include_router(auth_router)
    router.include_router(teams_router)
    router.include_router(tasks_router)
    router.include_router(task_comments_router)


include_routers()
