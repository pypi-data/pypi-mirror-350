from enum import Enum


class GetListOfComputableModelsStatusesItem(str, Enum):
    ARCHIVED = "ARCHIVED"
    DRAFT = "DRAFT"
    RELEASED = "RELEASED"

    def __str__(self) -> str:
        return str(self.value)
