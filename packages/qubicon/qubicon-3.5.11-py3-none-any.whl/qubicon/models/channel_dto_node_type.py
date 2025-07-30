from enum import Enum


class ChannelDtoNodeType(str, Enum):
    ACTOR = "ACTOR"
    METAINFO = "METAINFO"
    SENSOR = "SENSOR"
    SETPOINT = "SETPOINT"
    STATE = "STATE"

    def __str__(self) -> str:
        return str(self.value)
