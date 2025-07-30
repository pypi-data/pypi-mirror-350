from enum import Enum


class RoleDtoName(str, Enum):
    ADMIN = "ADMIN"
    API = "API"
    MANAGER = "MANAGER"
    MONITOR = "MONITOR"
    SUPER = "SUPER"
    USER = "USER"

    def __str__(self) -> str:
        return str(self.value)
