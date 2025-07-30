from enum import Enum


class GetOnlineEquipmentsStatusesItem(str, Enum):
    DEACTIVATED = "DEACTIVATED"
    DRAFT = "DRAFT"
    GMP = "GMP"
    IN_USE = "IN_USE"
    READY = "READY"

    def __str__(self) -> str:
        return str(self.value)
