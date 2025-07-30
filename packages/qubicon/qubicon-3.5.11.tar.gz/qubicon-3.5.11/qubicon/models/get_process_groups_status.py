from enum import Enum


class GetProcessGroupsStatus(str, Enum):
    ARCHIVED = "ARCHIVED"
    RELEASED = "RELEASED"

    def __str__(self) -> str:
        return str(self.value)
