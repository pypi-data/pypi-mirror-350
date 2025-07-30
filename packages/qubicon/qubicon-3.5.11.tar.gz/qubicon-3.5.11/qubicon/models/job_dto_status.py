from enum import Enum


class JobDtoStatus(str, Enum):
    CANCELATION_PENDING = "CANCELATION_PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    PLANNED = "PLANNED"

    def __str__(self) -> str:
        return str(self.value)
