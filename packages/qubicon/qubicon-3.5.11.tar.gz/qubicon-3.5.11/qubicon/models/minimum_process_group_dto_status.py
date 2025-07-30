from enum import Enum


class MinimumProcessGroupDtoStatus(str, Enum):
    ARCHIVED = "ARCHIVED"
    RELEASED = "RELEASED"

    def __str__(self) -> str:
        return str(self.value)
