from enum import Enum


class UserDtoLoginType(str, Enum):
    INTERNAL = "INTERNAL"
    LDAP = "LDAP"
    OAUTH = "OAUTH"

    def __str__(self) -> str:
        return str(self.value)
