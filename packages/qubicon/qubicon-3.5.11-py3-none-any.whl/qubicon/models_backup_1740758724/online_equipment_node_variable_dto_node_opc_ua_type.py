from enum import Enum


class OnlineEquipmentNodeVariableDtoNodeOpcUaType(str, Enum):
    DATATYPE = "DataType"
    METHOD = "Method"
    OBJECT = "Object"
    VARIABLE = "Variable"
    VARIABLETYPE = "VariableType"

    def __str__(self) -> str:
        return str(self.value)
