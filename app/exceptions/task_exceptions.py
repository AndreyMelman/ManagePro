from .base_exceptions import ServiceError


class TaskNotTeamError(ServiceError):
    pass


class TaskNotFoundError(ServiceError):
    pass


class TaskPermissionError(ServiceError):
    pass


class InvalidAssigneeError(ServiceError):
    pass


class TaskCommentPermissionError(ServiceError):
    pass


class TaskCommentOwnerError(ServiceError):
    pass
