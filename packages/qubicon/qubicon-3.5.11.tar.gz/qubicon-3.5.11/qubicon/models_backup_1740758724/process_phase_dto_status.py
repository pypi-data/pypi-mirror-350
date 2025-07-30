from enum import Enum


class ProcessPhaseDtoStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NOT_READY = "NOT_READY"
    READY = "READY"
    RUNNING = "RUNNING"

    def __str__(self) -> str:
        return str(self.value)
