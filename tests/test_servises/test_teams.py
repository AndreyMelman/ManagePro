import pytest
from core.models import User, Team
from core.schemas.team import TeamCreateSchema
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole
from crud.teams import TeamService


@pytest.mark.asyncio
async def test_create_team_sets_admin_and_team_id(session):
    user = User(email="admin@ex.com", role=UserRole.ADMIN)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = TeamService(session)
    team_in = TeamCreateSchema(name="TestTeam", code="TST")
    team = await crud.create_team(team_in, user)

    assert team.admin_id == user.id
    await session.refresh(user)
    assert user.team_id == team.id


@pytest.mark.asyncio
async def test_add_user_to_team(session):
    team = Team(name="Team1", code="T1", admin_id=1)
    user = User(email="user@ex.com", role=UserRole.USER)
    session.add_all([team, user])
    await session.commit()
    await session.refresh(team)
    await session.refresh(user)

    crud = TeamService(session)
    await crud.add_user_to_team(team, user)
    await session.refresh(user)
    assert user.team_id == team.id


@pytest.mark.asyncio
async def test_update_user_team_role(session):
    user = User(email="user2@ex.com", role=UserRole.USER)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = TeamService(session)
    role_data = UpdateRoleRequest(role=UserRole.MANAGER)
    await crud.update_user_team_role(user, role_data)
    await session.refresh(user)
    assert user.role == UserRole.MANAGER


@pytest.mark.asyncio
async def test_remove_user_from_team(session):
    team = Team(name="Team2", code="T2", admin_id=1)
    user = User(email="user3@ex.com", role=UserRole.MANAGER, team_id=1)
    session.add_all([team, user])
    await session.commit()
    await session.refresh(user)

    crud = TeamService(session)
    await crud.remove_user_from_team(user)
    await session.refresh(user)
    assert user.team_id is None
    assert user.role == UserRole.USER


@pytest.mark.asyncio
async def test_get_team(session):
    user = User(email="admin2@ex.com", role=UserRole.ADMIN)
    team = Team(name="Team3", code="T3", admin_id=1)
    session.add_all([user, team])
    await session.commit()
    await session.refresh(user)
    await session.refresh(team)

    crud = TeamService(session)
    result = await crud.get_team(team_id=team.id, user=user)
    assert result.id == team.id


@pytest.mark.asyncio
async def test_get_team_with_users(session):
    team = Team(name="Team4", code="T4", admin_id=1)
    user1 = User(email="user4@ex.com", role=UserRole.USER, team=team)
    user2 = User(email="user5@ex.com", role=UserRole.MANAGER, team=team)
    session.add_all([team, user1, user2])
    await session.commit()
    await session.refresh(team)

    crud = TeamService(session)
    result = await crud.get_team_with_users(team, role_filter=UserRole.USER)
    assert result.id == team.id
    assert len(result.users) == 2
