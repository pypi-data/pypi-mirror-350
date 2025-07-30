from enum import Enum


class AbstractComputableModelDtoCalculationStyle(str, Enum):
    ONLINE = "ONLINE"
    SAMPLING = "SAMPLING"
    SAMPLING_ORDERED = "SAMPLING_ORDERED"

    def __str__(self) -> str:
        return str(self.value)
