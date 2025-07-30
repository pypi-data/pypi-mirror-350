from enum import Enum


class ProcessDtoType(str, Enum):
    GOLDEN = "GOLDEN"
    IMPORT = "IMPORT"
    LIVE = "LIVE"
    MASTER = "MASTER"
    NORMAL = "NORMAL"

    def __str__(self) -> str:
        return str(self.value)
