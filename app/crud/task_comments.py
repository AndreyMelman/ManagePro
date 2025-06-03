from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, User, TaskComment
from core.schemas.task_comment import TaskCommentCreateSchema, TaskCommentUpdateSchema
from crud.validators.task_validators import (
    check_user_command,
    check_task_owner,
    check_task_comment_owner,
)


class TaskCommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_comments(
        self,
        task: Task,
        current_user: User,
    ) -> list[TaskComment]:
        check_user_command(user=current_user, task=task)

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
        current_user: User,
        comment_id: int,
    ) -> TaskComment:
        check_user_command(user=current_user, task=task)
        stmt = select(TaskComment).where(TaskComment.task_id == task.id, TaskComment.id == comment_id,)
        result: Result = await self.session.execute(stmt)
        comment = result.scalars().first()
        return comment

    async def create_task_comment(
        self,
        task: Task,
        current_user: User,
        comment_in: TaskCommentCreateSchema,
    ) -> TaskComment:

        comment = TaskComment(
            **comment_in.model_dump(),
            task_id=task.id,
            user_id=current_user.id,
        )

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def update_task_comment(
        self,
        comment: TaskComment,
        current_user: User,
        comment_update: TaskCommentUpdateSchema,
    ) -> TaskComment:
        check_task_comment_owner(current_user, comment)

        update_data = comment_update.model_dump()
        for name, value in update_data.items():
            setattr(comment, name, value)

        await self.session.commit()
        await self.session.refresh(comment)

        return comment

    async def delete_task_comment(
        self,
        comment: TaskComment,
        current_user: User,
    ) -> None:
        check_task_comment_owner(current_user, comment)

        await self.session.delete(comment)
        await self.session.commit()
