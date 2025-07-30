from enum import Enum


class UserLoginDtoLoginType(str, Enum):
    INTERNAL = "INTERNAL"
    LDAP = "LDAP"
    OAUTH = "OAUTH"

    def __str__(self) -> str:
        return str(self.value)
