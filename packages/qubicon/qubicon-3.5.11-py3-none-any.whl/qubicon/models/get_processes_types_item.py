from enum import Enum


class GetProcessesTypesItem(str, Enum):
    GOLDEN = "GOLDEN"
    IMPORT = "IMPORT"
    LIVE = "LIVE"
    MASTER = "MASTER"
    NORMAL = "NORMAL"

    def __str__(self) -> str:
        return str(self.value)
