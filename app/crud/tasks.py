from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.task_exceptions import TaskNotTeamError
from core.models import User, Task
from core.schemas.task import TaskCreateShema, TaskUpdateShema


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(
        self,
        current_user: User,
        task_in: TaskCreateShema,
    ) -> Task:
        if not current_user.team_id:
            raise TaskNotTeamError()

        task = Task(
            **task_in.model_dump(),
            creator_id=current_user.id,
            team_id=current_user.team_id,
        )
        self.session.add(task)
        await self.session.commit()

        return task

    async def update_task(
        self,
        current_user: User,
        task_update: TaskUpdateShema,
        partial: bool = False,
    ) -> Task:
        for name, value in task_update.model_dump(exclude_unset=partial).items():
            setattr(task, name, value)

        await self.session.commit()
        return task
