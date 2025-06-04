from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Evaluation, User, Task
from core.schemas.evaluation import (
    EvaluationCreateSchema,
)
from crud.validators.evaluation_validators import already_estimated


class EvaluationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_evaluation(
        self,
        evaluation_in: EvaluationCreateSchema,
        current_user: User,
        task: Task,
    ) -> Evaluation:
        stmt = select(Evaluation).where(
            Evaluation.task_id == task.id, Evaluation.evaluator_id == current_user.id
        )
        existing_evaluation = await self.session.execute(stmt)

        already_estimated(existing_evaluation)

        evaluation = Evaluation(
            **evaluation_in.model_dump(),
            evaluator_id=current_user.id,
            task_id=task.id,
            user_id=task.assignee_id,
        )

        self.session.add(evaluation)
        await self.session.commit()
        await self.session.refresh(evaluation)
        return evaluation
