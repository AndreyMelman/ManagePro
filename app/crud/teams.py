from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    with_loader_criteria,
)
from core.models import User, Team
from .validators.team_validators import (
    validate_team_access,
    check_team_admin,
    ensure_user_is_admin,
    disallow_admin_assignment,
    remove_team_admin,
)
from .validators.user_validators import (
    ensure_user_not_in_team,
    ensure_user_in_team,
)
from core.schemas.team import TeamCreateSchema
from exceptions.team_exceptions import (
    TeamCodeExistsError,
)
from exceptions.user_exceptions import UserNotFoundError
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user(
        self,
        user_id: int,
    ) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def get_team(
        self,
        team_id: int,
        user: User,
    ) -> Team:
        stmt = select(Team).where(
            Team.id == team_id,
            Team.admin_id == user.id,
        )
        result: Result = await self.session.execute(stmt)
        team = result.scalars().first()
        return team

    async def get_team_with_users(
        self,
        team: Team,
        user: User,
        role_filter: UserRole,
    ) -> Team:
        validate_team_access(user, team)

        stmt = select(Team).where(Team.id == team.id).options(selectinload(Team.users))

        if role_filter:
            stmt = stmt.options(with_loader_criteria(User, User.role == role_filter))

        result = await self.session.execute(stmt)
        team = result.scalar_one_or_none()

        return team

    async def create_team(
        self,
        team_in: TeamCreateSchema,
        user: User,
    ) -> Team:
        ensure_user_is_admin(user)
        ensure_user_not_in_team(user)

        team = Team(**team_in.model_dump(), admin_id=user.id)
        try:
            self.session.add(team)
            await self.session.flush()

            user.team_id = team.id
            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()
            raise TeamCodeExistsError()

        return team

    async def add_user_to_team(
        self,
        team: Team,
        user: User,
        user_id: int,
    ) -> None:
        user = await self._get_user(user_id)
        check_team_admin(user, team)
        ensure_user_not_in_team(user)

        user.team_id = team.id
        await self.session.commit()

    async def update_user_team_role(
        self,
        team: Team,
        user: User,
        role_data: UpdateRoleRequest,
        user_id: int,
    ) -> None:
        current_user = await self._get_user(user_id)

        check_team_admin(user, team)
        ensure_user_in_team(current_user, team)
        disallow_admin_assignment(role_data)

        user.role = role_data.role
        await self.session.commit()

    async def remove_user_from_team(
        self,
        team: Team,
        user: User,
        user_id: int,
    ) -> None:
        user = await self._get_user(user_id)

        validate_team_access(user, team)
        ensure_user_in_team(user, team)
        remove_team_admin(user, team)

        user.team_id = None
        user.role = UserRole.USER
        await self.session.commit()
