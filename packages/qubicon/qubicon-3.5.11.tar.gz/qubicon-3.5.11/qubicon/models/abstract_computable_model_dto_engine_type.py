from enum import Enum


class AbstractComputableModelDtoEngineType(str, Enum):
    EXTERNAL_PYTHON = "EXTERNAL_PYTHON"
    JYTHON = "JYTHON"

    def __str__(self) -> str:
        return str(self.value)
