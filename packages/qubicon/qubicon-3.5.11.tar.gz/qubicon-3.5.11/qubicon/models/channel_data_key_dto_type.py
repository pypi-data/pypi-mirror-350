from enum import Enum


class ChannelDataKeyDtoType(str, Enum):
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    SETPOINT = "SETPOINT"
    TAG = "TAG"

    def __str__(self) -> str:
        return str(self.value)
