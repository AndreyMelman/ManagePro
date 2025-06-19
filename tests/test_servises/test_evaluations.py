from datetime import datetime, timedelta

import pytest
from core.models import User, Task, Evaluation
from core.types.role import UserRole
from core.schemas.evaluation import EvaluationCreateSchema
from crud.evaluations import EvaluationService


@pytest.mark.asyncio
async def test_create_evaluation(session):
    evaluator = User(email="eval@ex.com", role=UserRole.USER, team_id=1)
    assignee = User(email="assignee@ex.com", role=UserRole.USER, team_id=1)
    session.add_all([evaluator, assignee])
    await session.commit()
    await session.refresh(evaluator)
    await session.refresh(assignee)

    task = Task(
        title="TaskEval",
        description="desc",
        creator_id=evaluator.id,
        team_id=1,
        assignee_id=assignee.id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    crud = EvaluationService(session)
    eval_in = EvaluationCreateSchema(score=5, comment="Отлично")
    evaluation = await crud.create_evaluation(eval_in, evaluator, task)

    assert evaluation.score == 5
    assert evaluation.comment == "Отлично"
    assert evaluation.evaluator_id == evaluator.id
    assert evaluation.task_id == task.id
    assert evaluation.user_id == assignee.id


@pytest.mark.asyncio
async def test_get_evaluations(session):
    user = User(email="eval2@ex.com", role=UserRole.USER, team_id=2)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    task = Task(
        title="TaskEval2",
        description="desc2",
        creator_id=user.id,
        team_id=2,
        assignee_id=user.id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    eval1 = Evaluation(
        score=4,
        comment="Хорошо",
        evaluator_id=user.id,
        user_id=user.id,
        task_id=task.id,
    )
    eval2 = Evaluation(
        score=5,
        comment="Отлично",
        evaluator_id=user.id,
        user_id=user.id,
        task_id=task.id,
    )
    session.add_all([eval1, eval2])
    await session.commit()

    crud = EvaluationService(session)
    evaluations = await crud.get_evaluations(user)
    assert len(evaluations) == 2
    assert any(e.score == 4 for e in evaluations)
    assert any(e.score == 5 for e in evaluations)


@pytest.mark.asyncio
async def test_get_average_score(session):
    user = User(email="eval3@ex.com", role=UserRole.USER, team_id=3)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    task = Task(
        title="TaskEval3",
        description="desc3",
        creator_id=user.id,
        team_id=3,
        assignee_id=user.id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    now = datetime.now()
    eval1 = Evaluation(
        score=3,
        comment="OK",
        evaluator_id=user.id,
        user_id=user.id,
        task_id=task.id,
        created_at=now,
    )
    eval2 = Evaluation(
        score=5,
        comment="Super",
        evaluator_id=user.id,
        user_id=user.id,
        task_id=task.id,
        created_at=now - timedelta(days=1),
    )
    session.add_all([eval1, eval2])
    await session.commit()

    crud = EvaluationService(session)
    avg = await crud.get_average_score(user)
    assert avg == 4

    avg_today = await crud.get_average_score(user, start_date=now.date())
    assert avg_today == 3


import pytest
from exceptions.evaluation_exceptions import DuplicateEstimateError


@pytest.mark.asyncio
async def test_create_evaluation_duplicate(session):
    evaluator = User(email="eval4@ex.com", role=UserRole.USER, team_id=4)
    assignee = User(email="assignee4@ex.com", role=UserRole.USER, team_id=4)
    session.add_all([evaluator, assignee])
    await session.commit()
    await session.refresh(evaluator)
    await session.refresh(assignee)

    task = Task(
        title="TaskEval4",
        description="desc",
        creator_id=evaluator.id,
        team_id=4,
        assignee_id=assignee.id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    crud = EvaluationService(session)
    eval_in = EvaluationCreateSchema(score=5, comment="Отлично")
    await crud.create_evaluation(eval_in, evaluator, task)

    with pytest.raises(DuplicateEstimateError):
        await crud.create_evaluation(eval_in, evaluator, task)
