from enum import Enum


class ProcessPhaseDtoType(str, Enum):
    POST = "POST"
    PRE = "PRE"
    PROCESS = "PROCESS"

    def __str__(self) -> str:
        return str(self.value)
