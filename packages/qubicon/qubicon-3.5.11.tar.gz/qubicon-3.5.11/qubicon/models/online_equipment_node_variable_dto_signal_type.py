from enum import Enum


class OnlineEquipmentNodeVariableDtoSignalType(str, Enum):
    CALIBRATION = "CALIBRATION"
    DATA = "DATA"
    STATE = "STATE"

    def __str__(self) -> str:
        return str(self.value)
