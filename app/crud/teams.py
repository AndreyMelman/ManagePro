from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    with_loader_criteria,
)
from core.models import User, Team
from core.schemas.team import TeamCreateSchema
from exceptions.team_exceptions import (
    TeamCodeExistsError,
)
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_team(
        self,
        team_id: int,
        user: User,
    ) -> Team:
        stmt = select(Team).where(
            Team.id == team_id,
        ).options(selectinload(Team.users))
        result: Result = await self.session.execute(stmt)
        team = result.scalars().first()
        return team

    async def get_team_with_users(
        self,
        team: Team,
        role_filter: UserRole,
    ) -> Team:
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
    ) -> None:
        user.team_id = team.id
        await self.session.commit()

    async def update_user_team_role(
        self,
        user: User,
        role_data: UpdateRoleRequest,
    ) -> None:
        user.role = role_data.role
        await self.session.commit()

    async def remove_user_from_team(
        self,
        user: User,
    ) -> None:
        user.team_id = None
        user.role = UserRole.USER
        await self.session.commit()
