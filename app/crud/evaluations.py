from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    Evaluation,
    User,
    Task,
)
from core.schemas.evaluation import (
    EvaluationCreateSchema,
)
from crud.validators.evaluation_validators import already_estimated, is_task_completed


class EvaluationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_evaluations(
        self,
        current_user: User,
    ) -> list[Evaluation]:
        stmt = (
            select(Evaluation)
            .where(Evaluation.user_id == current_user.id)
            .order_by(Evaluation.id)
        )
        result = await self.session.execute(stmt)
        evaluations = result.scalars().all()
        return list(evaluations)

    async def get_average_score(
        self,
        current_user: User,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> float:
        stmt = select(func.avg(Evaluation.score)).where(Evaluation.user_id == current_user.id)

        if start_date:
            stmt = stmt.where(Evaluation.created_at >= start_date)

        if end_date:
            stmt = stmt.where(Evaluation.created_at <= end_date)

        result = await self.session.execute(stmt)
        return result.scalar() or 0.0

    async def create_evaluation(
        self,
        evaluation_in: EvaluationCreateSchema,
        current_user: User,
        task: Task,
    ) -> Evaluation:
        is_task_completed(task=task)

        stmt = select(Evaluation).where(
            Evaluation.task_id == task.id,
            Evaluation.evaluator_id == current_user.id,
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
