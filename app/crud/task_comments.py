from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, User, TaskComment
from core.schemas.task_comment import TaskCommentCreateSchema
from crud.validators.task_validators import check_user_command, check_task_owner


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

        result = await self.session.execute(stmt)

        comments = result.scalars().all()
        return list(comments)


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