from .base_exceptions import ServiceError


class TeamNotFoundError(ServiceError):
    pass


class TeamAccessDeniedError(ServiceError):
    pass


class TeamAdminRequiredError(ServiceError):
    def __init__(self, team_name: str):
        self.team_name = team_name


class CannotRemoveTeamAdminError(ServiceError):
    pass


class TeamCodeExistsError(ServiceError):
    pass


class CannotAddTeamAdminError(ServiceError):
    pass


class TeamAdminError(ServiceError):
    pass


class TaskCommentNotFoundError(ServiceError):
    pass
