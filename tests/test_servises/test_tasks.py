import pytest
from core.models import User, Task
from core.types.role import UserRole
from core.schemas.task import TaskCreateShema
from crud.tasks import TaskService


@pytest.mark.asyncio
async def test_create_task(session):
    user = User(email="user@ex.com", role=UserRole.USER, team_id=1)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = TaskService(session)
    task_in = TaskCreateShema(title="Test Task", description="desc")
    task = await crud.create_task(user, task_in)

    assert task.creator_id == user.id
    assert task.team_id == user.team_id
    assert task.title == "Test Task"
    assert task.description == "desc"


@pytest.mark.asyncio
async def test_get_task(session):
    user = User(email="user2@ex.com", role=UserRole.USER, team_id=2)
    task = Task(title="Task2", description="desc2", creator_id=1, team_id=2)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(user)
    await session.refresh(task)

    crud = TaskService(session)
    result = await crud.get_task(user, task.id)
    assert result.id == task.id
    assert result.team_id == user.team_id


@pytest.mark.asyncio
async def test_update_task(session):
    user = User(email="user3@ex.com", role=UserRole.USER, team_id=3)
    task = Task(title="Task3", description="desc3", creator_id=1, team_id=3)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskService(session)
    update_data = {"title": "Updated Task", "description": "new desc"}
    updated_task = await crud.update_task(task, update_data)
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "new desc"


@pytest.mark.asyncio
async def test_update_task_with_assignee(session):
    user = User(email="user4@ex.com", role=UserRole.USER, team_id=4)
    assignee = User(email="assignee@ex.com", role=UserRole.USER, team_id=4)
    task = Task(title="Task4", description="desc4", creator_id=1, team_id=4)
    session.add_all([user, assignee, task])
    await session.commit()
    await session.refresh(task)
    await session.refresh(assignee)

    crud = TaskService(session)
    update_data = {"title": "Task with Assignee"}
    updated_task = await crud.update_task(task, update_data, assignee=assignee)
    assert updated_task.title == "Task with Assignee"
    assert updated_task.assignee_id == assignee.id


@pytest.mark.asyncio
async def test_delete_task(session):
    user = User(email="user5@ex.com", role=UserRole.USER, team_id=5)
    task = Task(title="Task5", description="desc5", creator_id=1, team_id=5)
    session.add_all([user, task])
    await session.commit()
    await session.refresh(task)

    crud = TaskService(session)
    await crud.delete_task(task)
    result = await session.get(Task, task.id)
    assert result is None
