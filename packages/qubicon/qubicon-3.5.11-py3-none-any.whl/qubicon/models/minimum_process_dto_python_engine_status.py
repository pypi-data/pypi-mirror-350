from enum import Enum


class MinimumProcessDtoPythonEngineStatus(str, Enum):
    AUTO_PROVIDED = "AUTO_PROVIDED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REQUESTED = "REQUESTED"
    UNUSED = "UNUSED"

    def __str__(self) -> str:
        return str(self.value)
