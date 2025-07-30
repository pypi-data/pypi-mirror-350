from enum import Enum


class GetListOfComputableModelsTypesItem(str, Enum):
    EXTERNAL_PYTHON = "EXTERNAL_PYTHON"
    JYTHON = "JYTHON"

    def __str__(self) -> str:
        return str(self.value)
