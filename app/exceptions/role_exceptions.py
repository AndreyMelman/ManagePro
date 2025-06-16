from .base_exceptions import ServiceError


class RoleError(ServiceError):
    """Базовое исключение для ошибок ролей"""

    def __init__(
        self,
        message: str = "User does not have required role",
        role: str | None = None,
        user_id: int | None = None,
    ):
        self.message = message
        self.role = role
        self.user_id = user_id
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.role and self.user_id:
            return f"{self.message} (User {self.user_id}, Required role: {self.role})"
        elif self.role:
            return f"{self.message} (Required role: {self.role})"
        elif self.user_id:
            return f"{self.message} (User {self.user_id})"
        return self.message


class AdminRequiredError(RoleError):
    """Требуется роль администратора"""

    def __init__(
        self, message: str = "User must be an admin", user_id: int | None = None
    ):
        super().__init__(message=message, role="admin", user_id=user_id)


class ManagerRequiredError(RoleError):
    """Требуется роль менеджера"""

    def __init__(
        self, message: str = "User must be a manager", user_id: int | None = None
    ):
        super().__init__(message=message, role="manager", user_id=user_id)


class UserRoleRequiredError(RoleError):
    """Требуется базовая роль пользователя"""

    def __init__(
        self,
        message: str = "User must have basic user role",
        user_id: int | None = None,
    ):
        super().__init__(message=message, role="user", user_id=user_id)


class InvalidRoleError(RoleError):
    """Недопустимая роль"""

    def __init__(
        self,
        role: str,
        message: str = "Invalid role specified",
        user_id: int | None = None,
    ):
        super().__init__(message=message, role=role, user_id=user_id)
