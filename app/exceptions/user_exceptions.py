from exceptions.base_exceptions import ServiceError


class UserNotFoundError(ServiceError):
    pass


class UserAlreadyInTeamError(ServiceError):
    def __init__(self, user_id: int):
        self.user_id = user_id


class UserNotInTeamError(ServiceError):
    pass
