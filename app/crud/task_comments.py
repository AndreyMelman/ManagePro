from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    Task,
    User,
    TaskComment,
)
from core.schemas.task_comment import (
    TaskCommentCreateSchema,
    TaskCommentUpdateSchema,
)


class TaskCommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_comments(
        self,
        task: Task,
    ) -> list[TaskComment]:
        stmt = (
            select(TaskComment)
            .where(TaskComment.task_id == task.id)
            .order_by(TaskComment.created_at.desc())
        )

        result: Result = await self.session.execute(stmt)

        comments = result.scalars().all()
        return list(comments)

    async def get_task_comment(
        self,
        task: Task,
        comment_id: int,
    ) -> TaskComment:
        stmt = select(TaskComment).where(
            TaskComment.task_id == task.id,
            TaskComment.id == comment_id,
        )
        result: Result = await self.session.execute(stmt)
        comment = result.scalars().first()
        return comment

    async def create_task_comment(
        self,
        task: Task,
        user: User,
        comment_in: TaskCommentCreateSchema,
    ) -> TaskComment:
        comment = TaskComment(
            **comment_in.model_dump(),
            task_id=task.id,
            user_id=user.id,
        )

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def update_task_comment(
        self,
        comment: TaskComment,
        comment_update: TaskCommentUpdateSchema,
    ) -> TaskComment:
        update_data = comment_update.model_dump()
        for name, value in update_data.items():
            setattr(comment, name, value)

        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def delete_task_comment(
        self,
        comment: TaskComment,
    ) -> None:
        await self.session.delete(comment)
        await self.session.commit()
