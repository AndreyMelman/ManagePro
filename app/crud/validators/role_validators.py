from core.models import User
from core.types.role import UserRole
from exceptions.role_exceptions import (
    RoleError,
    AdminRequiredError,
    ManagerRequiredError,
    UserRoleRequiredError,
)


def ensure_user_role(
    user: User,
    required_roles: UserRole | list[UserRole],
    error_message: str = "User does not have required role",
) -> None:
    """
    Проверяет, имеет ли пользователь требуемую роль.

    Args:
        user: Пользователь для проверки
        required_roles: Требуемая роль или список ролей
        error_message: Сообщение об ошибке (опционально)

    Raises:
        RoleError: Если пользователь не имеет требуемой роли
    """
    if isinstance(required_roles, UserRole):
        required_roles = [required_roles]

    if user.role not in required_roles:
        if UserRole.ADMIN in required_roles:
            raise AdminRequiredError(user_id=user.id)
        elif UserRole.MANAGER in required_roles:
            raise ManagerRequiredError(user_id=user.id)
        elif UserRole.USER in required_roles:
            raise UserRoleRequiredError(user_id=user.id)
        else:
            raise RoleError(
                message=error_message, role=str(required_roles), user_id=user.id
            )
