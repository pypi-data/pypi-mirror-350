from enum import Enum


class GetProcessesStatusesItem(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    READY = "READY"
    RUNNING = "RUNNING"
    WARMING_UP = "WARMING_UP"

    def __str__(self) -> str:
        return str(self.value)
