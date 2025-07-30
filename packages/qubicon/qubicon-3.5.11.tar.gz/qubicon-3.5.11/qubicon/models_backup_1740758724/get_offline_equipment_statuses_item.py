from enum import Enum


class GetOfflineEquipmentStatusesItem(str, Enum):
    AUTO_IMPORT = "AUTO_IMPORT"
    DEACTIVATED = "DEACTIVATED"
    DRAFT = "DRAFT"
    GMP = "GMP"
    READY = "READY"

    def __str__(self) -> str:
        return str(self.value)
