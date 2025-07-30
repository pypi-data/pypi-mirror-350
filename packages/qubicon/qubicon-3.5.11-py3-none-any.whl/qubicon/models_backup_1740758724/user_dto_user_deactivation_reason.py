from enum import Enum


class UserDtoUserDeactivationReason(str, Enum):
    MANUAL = "MANUAL"
    TOO_LONG_INACTIVITY_PERIOD = "TOO_LONG_INACTIVITY_PERIOD"
    TOO_MANY_FAILED_LOGIN_ATTEMPTS = "TOO_MANY_FAILED_LOGIN_ATTEMPTS"

    def __str__(self) -> str:
        return str(self.value)
