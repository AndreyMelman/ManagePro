from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, Team
from core.schemas.team import TeamCreateSchema


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_team(
        self,
        team_in: TeamCreateSchema,
        user: User,
    ) -> Team:
        team = Team(**team_in.model_dump(), admin_id=user.id)
        try:
            self.session.add(team)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="Team code already exists")
        return team

    async def add_user_to_team(
        self,
        team_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        team = await self.session.get(Team, team_id)
        user = await self.session.get(User, user_id)

        if not team or not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Команда или юзер не найдены",
            )

        if team.admin_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Только админ команды {team.name} может добавлять участников",
            )

        if user.team_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"У пользователя {user.id} уже есть команда",
            )

        user.team_id = team_id
        await self.session.commit()
