import pytest
from core.models import User, Task
from core.types.role import UserRole
from core.schemas.task_comment import TaskCommentCreateSchema
from crud.task_comments import TaskCommentService


@pytest.mark.asyncio
async def test_create_task_comment(session):
    user = User(email="user@ex.com", role=UserRole.USER, team_id=1)
    task = Task(title="Task", description="desc", creator_id=1, team_id=1)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(user)
    await session.refresh(task)

    crud = TaskCommentService(session)
    comment_in = TaskCommentCreateSchema(content="Комментарий")
    comment = await crud.create_task_comment(task, user, comment_in)

    assert comment.content == "Комментарий"
    assert comment.user_id == user.id
    assert comment.task_id == task.id


@pytest.mark.asyncio
async def test_get_task_comments(session):
    user = User(email="user2@ex.com", role=UserRole.USER, team_id=2)
    task = Task(title="Task2", description="desc2", creator_id=1, team_id=2)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskCommentService(session)

    await crud.create_task_comment(
        task, user, TaskCommentCreateSchema(content="Первый")
    )
    await crud.create_task_comment(
        task, user, TaskCommentCreateSchema(content="Второй")
    )

    comments = await crud.get_task_comments(task)
    assert len(comments) == 2
    assert comments[0].content in ["Первый", "Второй"]
    assert comments[1].content in ["Первый", "Второй"]


@pytest.mark.asyncio
async def test_get_task_comment(session):
    user = User(email="user3@ex.com", role=UserRole.USER, team_id=3)
    task = Task(title="Task3", description="desc3", creator_id=1, team_id=3)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskCommentService(session)
    comment = await crud.create_task_comment(
        task, user, TaskCommentCreateSchema(content="Один")
    )
    found = await crud.get_task_comment(task, comment.id)
    assert found.id == comment.id
    assert found.content == "Один"


from core.schemas.task_comment import TaskCommentUpdateSchema


@pytest.mark.asyncio
async def test_update_task_comment(session):
    user = User(email="user4@ex.com", role=UserRole.USER, team_id=4)
    task = Task(title="Task4", description="desc4", creator_id=1, team_id=4)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskCommentService(session)
    comment = await crud.create_task_comment(
        task, user, TaskCommentCreateSchema(content="Старый")
    )
    update_in = TaskCommentUpdateSchema(content="Новый")
    updated = await crud.update_task_comment(comment, update_in)
    assert updated.content == "Новый"


@pytest.mark.asyncio
async def test_delete_task_comment(session):
    user = User(email="user5@ex.com", role=UserRole.USER, team_id=5)
    task = Task(title="Task5", description="desc5", creator_id=1, team_id=5)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskCommentService(session)
    comment = await crud.create_task_comment(
        task, user, TaskCommentCreateSchema(content="Удалить")
    )
    await crud.delete_task_comment(comment)

    found = await crud.get_task_comment(task, comment.id)
    assert found is None
