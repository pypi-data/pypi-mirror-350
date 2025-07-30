from enum import Enum


class PhysicalQuantityUnitDtoStatus(str, Enum):
    IN_USE = "IN_USE"
    READY = "READY"

    def __str__(self) -> str:
        return str(self.value)
