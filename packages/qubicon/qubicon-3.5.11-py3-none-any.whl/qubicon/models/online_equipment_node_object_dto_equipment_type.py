from enum import Enum


class OnlineEquipmentNodeObjectDtoEquipmentType(str, Enum):
    ACTOR = "ACTOR"
    METAINFO = "METAINFO"
    SENSOR = "SENSOR"
    SETPOINT = "SETPOINT"
    STATE = "STATE"

    def __str__(self) -> str:
        return str(self.value)
