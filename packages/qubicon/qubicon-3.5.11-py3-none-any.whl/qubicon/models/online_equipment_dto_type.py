from enum import Enum


class OnlineEquipmentDtoType(str, Enum):
    EQUIPMENT = "EQUIPMENT"
    EQUIPMENT_ROOT = "EQUIPMENT_ROOT"
    FOLDER = "FOLDER"

    def __str__(self) -> str:
        return str(self.value)
