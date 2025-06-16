from .base_exceptions import ServiceError


class MeetingNotFoundError(ServiceError):
    pass


class MeetingPermissionError(ServiceError):
    pass


class MeetingTimeConflictError(ServiceError):
    pass


class MeetingParticipantError(ServiceError):
    pass


class MeetingParticipantValidationError(ServiceError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
