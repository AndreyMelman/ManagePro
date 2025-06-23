from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    Result,
)
from core.models import (
    User,
    Task,
)
from core.schemas.task import TaskCreateShema


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(
        self,
        user: User,
    ) -> list[Task]:
        stmt = select(Task).where(Task.team_id == user.team_id)
        result = await self.session.execute(stmt)
        tasks = result.scalars().all()
        return list(tasks)

    async def get_task(
        self,
        user: User,
        task_id: int,
    ) -> Task | None:

        stmt = select(Task).where(
            Task.id == task_id,
            Task.team_id == user.team_id,
        )
        result: Result = await self.session.execute(stmt)
        task = result.scalars().first()
        return task

    async def create_task(
        self,
        user: User,
        task_in: TaskCreateShema,
    ) -> Task:
        task = Task(
            **task_in.model_dump(),
            creator_id=user.id,
            team_id=user.team_id,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update_task(
        self,
        task: Task,
        update_data: dict,
        assignee: User | None = None,
    ) -> Task:
        for name, value in update_data.items():
            setattr(task, name, value)

        if assignee:
            task.assignee_id = assignee.id

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete_task(
        self,
        task: Task,
    ) -> None:
        await self.session.delete(task)
        await self.session.commit()
