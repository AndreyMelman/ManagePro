from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    with_loader_criteria,
)
from core.models import User, Team
from core.schemas.team import TeamCreateSchema
from exceptions.team_exceptions import (
    TeamNotFoundError,
    TeamAccessDeniedError,
    TeamAdminRequiredError,
    CannotRemoveTeamAdminError,
    TeamCodeExistsError,
    CannotAddTeamAdminError,
)
from exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyInTeamError,
    UserNotInTeamError,
)
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole


class TeamService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_team(
        self,
        team_id: int,
    ) -> type[Team]:
        """
        Получить команду по ID.

        Args:
            team_id: ID команды

        Returns:
            Team: Объект команды

        Raises:
            TeamNotFoundError: Если команда не найдена
        """
        team = await self.session.get(Team, team_id)
        if not team:
            raise TeamNotFoundError()
        return team

    async def _get_user(
        self,
        user_id: int,
    ) -> type[User]:
        """
        Получить пользователя по ID.

        Args:
            user_id: ID пользователя

        Returns:
            User: Объект пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден
        """
        user = await self.session.get(User, user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def _check_team_admin(
        self,
        team: Team,
        current_user: User,
    ) -> None:
        """
        Проверить, является ли пользователь администратором команды.

        Args:
            team: Объект команды
            current_user: Текущий администратор команды

        Raises:
            TeamAdminRequiredError: Если пользователь не является администратором команды
        """
        if team.admin_id != current_user.id:
            raise TeamAdminRequiredError(team.name)

    async def create_team(
        self,
        team_in: TeamCreateSchema,
        user: User,
    ) -> Team:
        """
        Создать новую команду.

        Args:
            team_in: Данные для создания команды
            user: Пользователь, создающий команду

        Returns:
            Team: Созданная команда

        Raises:
            UserAlreadyInTeamError: Если пользователь уже состоит в команде
            TeamCodeExistsError: Если код команды уже существует
        """
        if user.team_id is not None:
            raise UserAlreadyInTeamError(user.id)

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
        team_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        """
        Добавить пользователя в команду.

        Args:
            team_id: ID команды
            user_id: ID пользователя
            current_user: Текущий администратор команды

        Raises:
            TeamNotFoundError: Если команда не найдена
            UserNotFoundError: Если пользователь не найден
            TeamAdminRequiredError: Если текущий пользователь не является администратором команды
            UserAlreadyInTeamError: Если пользователь уже состоит в команде
        """
        team = await self._get_team(team_id)
        user = await self._get_user(user_id)
        await self._check_team_admin(team, current_user)

        if user.team_id is not None:
            raise UserAlreadyInTeamError(user.id)

        user.team_id = team_id
        await self.session.commit()

    async def update_user_team_role(
        self,
        user_id: int,
        team_id: int,
        current_user: User,
        role_data: UpdateRoleRequest,
    ) -> None:
        """
        Назначение ролей (менеджер, сотрудник)

        Args:
            team_id: ID команды
            user_id: ID пользователя
            current_user: Текущий администратор команды
            role_data: Данные для обновления роли

        Returns:
            None

        Raises:
            TeamNotFoundError: Если команда не найдена
            UserNotFoundError: Если пользователь не найден
            TeamAdminRequiredError: Если текущий пользователь не является администратором команды
            UserNotInTeamError: Если пользователь не состоит в команде
            CannotAddTeamAdmin: Если пытаемся назначить администратора
        """
        team = await self._get_team(team_id)
        user = await self._get_user(user_id)
        await self._check_team_admin(team, current_user)

        if user.team_id != team_id:
            raise UserNotInTeamError()

        if role_data.role == "admin":
            raise CannotAddTeamAdminError()

        user.role = role_data.role
        await self.session.commit()

    async def remove_user_from_team(
        self,
        team_id: int,
        user_id: int,
        current_user: User,
    ) -> None:
        """
        Удалить пользователя из команды.

        Args:
            team_id: ID команды
            user_id: ID пользователя
            current_user: Текущий администратор команды

        Raises:
            TeamNotFoundError: Если команда не найдена
            UserNotFoundError: Если пользователь не найден
            TeamAdminRequiredError: Если текущий пользователь не является администратором команды
            UserNotInTeamError: Если пользователь не состоит в команде
            CannotRemoveTeamAdminError: Если пытаемся удалить администратора команды
        """
        team = await self._get_team(team_id)
        user = await self._get_user(user_id)
        await self._check_team_admin(team, current_user)

        if user.team_id != team_id:
            raise UserNotInTeamError()

        if user.id == team.admin_id:
            raise CannotRemoveTeamAdminError()

        user.team_id = None
        await self.session.commit()

    async def get_team_with_users(
        self,
        team_id: int,
        current_user: User,
        role_filter: UserRole,
    ) -> Team:
        """
        Получить состав команды.

        Args:
            team_id: ID команды
            current_user: Текущий администратор команды
            role_filter: Фильтрация по роли

        Returns:
            Team: Команда с загруженными пользователями

        Raises:
            TeamAccessDeniedError: Если у пользователя нет доступа к команде
            TeamNotFoundError: Если команда не найдена
        """
        if current_user.team_id != team_id:
            raise TeamAccessDeniedError()

        stmt = select(Team).where(Team.id == team_id).options(selectinload(Team.users))

        if role_filter:
            stmt = stmt.options(with_loader_criteria(User, User.role == role_filter))

        result = await self.session.execute(stmt)
        team = result.scalar_one_or_none()

        if not team:
            raise TeamNotFoundError()

        return team
