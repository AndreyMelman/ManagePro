from typing import Any, Coroutine

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, Team
from core.schemas.team import TeamCreateSchema, TeamSchema


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_team(self, team_id: int) -> type[Team]:
        team = await self.session.get(Team, team_id)
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Команда не найдена",
            )
        return team

    async def _get_user(self, user_id: int) -> type[User]:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
        return user

    async def _check_team_admin(self, team: Team, current_user: User) -> None:
        if team.admin_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Только админ команды {team.name} может выполнять это действие",
            )

    async def create_team(
        self,
        team_in: TeamCreateSchema,
        user: User,
    ) -> Team:
        if user.team_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"У пользователя {user.id} уже есть команда",
            )
        team = Team(**team_in.model_dump(), admin_id=user.id)
        try:
            self.session.add(team)
            await self.session.flush()

            user.team_id = team.id
            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Код команды уже существует",
            )

        return team

    async def add_user_to_team(
        self,
        team_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        team = await self._get_team(team_id)
        user = await self._get_user(user_id)
        await self._check_team_admin(team, current_user)

        if user.team_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"У пользователя {user.id} уже есть команда",
            )

        user.team_id = team_id
        await self.session.commit()

    async def remove_user_from_team(
        self,
        team_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        team = await self._get_team(team_id)
        user = await self._get_user(user_id)
        await self._check_team_admin(team, current_user)

        if user.team_id != team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь не состоит в этой команде",
            )

        if user.id == team.admin_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Нельзя удалить админа команды",
            )

        user.team_id = None
        await self.session.commit()

    async def get_team_with_users(
        self,
        team_id: int,
        current_user: User,
    ) -> Team:
        """
        Получить состав команды.
        
        Args:
            team_id: ID команды
            current_user: Текущий пользователь
            
        Returns:
            list[TeamSchema]: Список с одной командой и её пользователями
            
        Raises:
            HTTPException: Если команда не найдена или у пользователя нет доступа
        """
        if current_user.team_id != team_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет доступа к этой команде",
            )

        stmt = (
            select(Team)
            .options(selectinload(Team.users))
            .where(Team.id == team_id)
        )
        result = await self.session.execute(stmt)
        team = result.scalar_one_or_none()

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Команда не найдена",
            )

        return team
