from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    Result,
)
from .validators.permissions import (
    ensure_user_has_team,
    check_task_owner,
)
from core.models import (
    User,
    Task,
)
from core.schemas.task import (
    TaskCreateShema,
    TaskUpdateShema,
)
from exceptions.task_exceptions import InvalidAssigneeError


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_team_user_by_id(
        self,
        user_id: int,
        team_id: int,
    ) -> User | None:
        stmt = select(User).where(
            User.id == user_id,
            User.team_id == team_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_task(
        self,
        current_user: User,
        task_id: int,
    ) -> Task | None:

        stmt = select(Task).where(
            Task.id == task_id,
            Task.creator_id == current_user.id,
        )
        result: Result = await self.session.execute(stmt)
        task = result.scalars().first()
        return task

    async def create_task(
        self,
        current_user: User,
        task_in: TaskCreateShema,
    ) -> Task:
        await ensure_user_has_team(current_user)

        if task_in.assignee_id is not None:
            assignee = await self._get_team_user_by_id(
                task_in.assignee_id, current_user.team_id
            )
            if assignee is None:
                raise InvalidAssigneeError()

        task = Task(
            **task_in.model_dump(),
            creator_id=current_user.id,
            team_id=current_user.team_id,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update_task(
        self,
        task: Task,
        current_user: User,
        task_update: TaskUpdateShema,
        partial: bool = False,
    ) -> Task:
        await check_task_owner(current_user, task)

        update_data = task_update.model_dump(exclude_unset=partial)

        assignee_id = update_data.get("assignee_id")
        if assignee_id is not None:
            assignee = await self._get_user_by_id(assignee_id)
            if not assignee or assignee.team_id != current_user.team_id:
                raise InvalidAssigneeError()

        for name, value in update_data.items():
            setattr(task, name, value)

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete_task(
        self,
        task: Task,
        current_user: User,
    ) -> None:
        await check_task_owner(current_user, task)

        await self.session.delete(task)
        await self.session.commit()
