from enum import Enum


class PhysicalQuantityDtoStatus(str, Enum):
    IN_USE = "IN_USE"
    READY = "READY"

    def __str__(self) -> str:
        return str(self.value)
