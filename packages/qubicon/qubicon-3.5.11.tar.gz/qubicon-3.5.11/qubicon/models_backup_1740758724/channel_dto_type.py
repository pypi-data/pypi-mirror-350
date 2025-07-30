from enum import Enum


class ChannelDtoType(str, Enum):
    KPI = "KPI"
    ONLINE = "ONLINE"
    TRIGGER = "TRIGGER"

    def __str__(self) -> str:
        return str(self.value)
