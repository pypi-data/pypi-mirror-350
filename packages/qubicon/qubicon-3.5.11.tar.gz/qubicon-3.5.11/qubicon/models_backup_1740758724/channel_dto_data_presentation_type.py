from enum import Enum


class ChannelDtoDataPresentationType(str, Enum):
    INTERPOLATION = "INTERPOLATION"
    INTERVAL = "INTERVAL"
    LIVE = "LIVE"

    def __str__(self) -> str:
        return str(self.value)
