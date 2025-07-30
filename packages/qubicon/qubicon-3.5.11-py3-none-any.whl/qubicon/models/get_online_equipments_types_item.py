from enum import Enum


class GetOnlineEquipmentsTypesItem(str, Enum):
    EQUIPMENT = "EQUIPMENT"
    EQUIPMENT_ROOT = "EQUIPMENT_ROOT"
    FOLDER = "FOLDER"

    def __str__(self) -> str:
        return str(self.value)
