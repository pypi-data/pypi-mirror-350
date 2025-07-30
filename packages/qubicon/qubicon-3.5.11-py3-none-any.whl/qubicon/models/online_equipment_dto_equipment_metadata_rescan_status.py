from enum import Enum


class OnlineEquipmentDtoEquipmentMetadataRescanStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROCESS = "IN_PROCESS"
    NEVER = "NEVER"

    def __str__(self) -> str:
        return str(self.value)
