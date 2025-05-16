from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    with_loader_criteria,
)
from core.models import User, Team
from .validators.permissions import (
    validate_team_access,
    check_team_admin,
    ensure_user_is_admin,
    ensure_user_not_in_team,
    ensure_user_in_team,
    disallow_admin_assignment,
    remove_team_admin,
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

    async def get_team(
        self,
        team_id: int,
        current_user: User,
    ) -> Team:
        """
        Получить состав команды.

        Args:
            team_id: ID команды
            current_user: Текущий администратор команды

        Returns:
            Team: Команда
        """
        stmt = select(Team).where(
            Team.id == team_id,
            Team.admin_id == current_user.id,
        )
        result: Result = await self.session.execute(stmt)
        team = result.scalars().first()
        return team

    async def get_team_with_users(
        self,
        team: Team,
        current_user: User,
        role_filter: UserRole,
    ) -> Team:
        """
        Получить состав команды.

        Args:
            team: Команда
            current_user: Текущий администратор команды
            role_filter: Фильтрация по роли

        Returns:
            Team: Команда с загруженными пользователями

        Raises:
            validate_team_access: Если текущий пользователь не является администратором команды
        """
        validate_team_access(current_user, team)

        stmt = select(Team).where(Team.id == team.id).options(selectinload(Team.users))

        if role_filter:
            stmt = stmt.options(with_loader_criteria(User, User.role == role_filter))

        result = await self.session.execute(stmt)
        team = result.scalar_one_or_none()

        return team

    async def create_team(
        self,
        team_in: TeamCreateSchema,
        current_user: User,
    ) -> Team:
        """
        Создать новую команду.

        Args:
            team_in: Данные для создания команды
            current_user: Администратор без команды, создающий команду

        Returns:
            Team: Созданная команда

        Raises:
            ensure_user_is_admin: Пользователь не является админом
            ensure_user_not_in_team: Если администратор уже состоит в команде
            TeamCodeExistsError: Если код команды уже существует
        """
        ensure_user_is_admin(current_user)
        ensure_user_not_in_team(current_user)

        team = Team(**team_in.model_dump(), admin_id=current_user.id)
        try:
            self.session.add(team)
            await self.session.flush()

            current_user.team_id = team.id
            await self.session.commit()

        except IntegrityError:
            await self.session.rollback()
            raise TeamCodeExistsError()

        return team

    async def add_user_to_team(
        self,
        team: Team,
        current_user: User,
        user_id: int,
    ) -> None:
        """
        Добавить пользователя в команду.

        Args:
            team: Команда в которую добавляется пользователь
            current_user: Текущий администратор команды
            user_id: ID пользователя

        Raises:
            check_team_admin: Если текущий пользователь не является администратором команды
            ensure_user_not_in_team: Если пользователь уже состоит в команде
        """
        user = await self._get_user(user_id)
        check_team_admin(current_user, team)
        ensure_user_not_in_team(user)

        user.team_id = team.id
        await self.session.commit()

    async def update_user_team_role(
        self,
        team: Team,
        current_user: User,
        role_data: UpdateRoleRequest,
        user_id: int,
    ) -> None:
        """
        Назначение ролей (менеджер, сотрудник)

        Args:
            team: Команда где нужно обновить роль пользователя
            current_user: Текущий администратор команды
            role_data: Данные для обновления роли
            user_id: ID пользователя

        Returns:
            None

        Raises:
            check_team_admin: Если текущий пользователь не является администратором команды
            ensure_user_in_team: Если пользователь не состоит в команде
            disallow_admin_assignment: Если пытаемся назначить администратора
        """
        user = await self._get_user(user_id)

        check_team_admin(current_user, team)
        ensure_user_in_team(user, team)
        disallow_admin_assignment(role_data)

        user.role = role_data.role
        await self.session.commit()

    async def remove_user_from_team(
        self,
        team: Team,
        current_user: User,
        user_id: int,
    ) -> None:
        """
        Удалить пользователя из команды.

        Args:
            team: Команда где нужно удалить пользователя
            current_user: Текущий администратор команды
            user_id: ID пользователя

        Raises:
            validate_team_access: Если текущий пользователь не является администратором команды
            ensure_user_in_team: Если пользователь не состоит в команде
            remove_team_admin: Если пытаемся удалить администратора команды
        """
        user = await self._get_user(user_id)

        validate_team_access(current_user, team)
        ensure_user_in_team(user, team)
        remove_team_admin(user, team)

        user.team_id = None
        user.role = UserRole.USER
        await self.session.commit()
