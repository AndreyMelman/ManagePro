from typing import Annotated

from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    get_manager,
    get_admin,
    current_active_superuser,
)
from api.dependencies.dependencies import make_crud_dependency
from core.models import User
from crud.calendars import CalendarService
from crud.meetings import MeetingService
from crud.task_comments import TaskCommentService
from crud.tasks import TaskService
from crud.teams import TeamService
from crud.users import UserService
from crud.evaluations import EvaluationService

TeamServiceDep = Annotated[TeamService, Depends(make_crud_dependency(TeamService))]
UserServiceDep = Annotated[UserService, Depends(make_crud_dependency(UserService))]
TaskServiceDep = Annotated[TaskService, Depends(make_crud_dependency(TaskService))]
TaskCommentServiceDep = Annotated[
    TaskCommentService, Depends(make_crud_dependency(TaskCommentService))
]
EvaluationServiceDep = Annotated[
    EvaluationService, Depends(make_crud_dependency(EvaluationService))
]
MeetingServiceDep = Annotated[
    MeetingService, Depends(make_crud_dependency(MeetingService))
]
CalendarServiceDep = Annotated[
    CalendarService, Depends(make_crud_dependency(CalendarService))
]

CurrentActiveUser = Annotated[User, Depends(current_active_user)]
CurrentActiveManager = Annotated[User, Depends(get_manager)]
CurrentActiveAdmin = Annotated[User, Depends(get_admin)]
CurrentActiveSuperUser = Annotated[User, Depends(current_active_superuser)]
