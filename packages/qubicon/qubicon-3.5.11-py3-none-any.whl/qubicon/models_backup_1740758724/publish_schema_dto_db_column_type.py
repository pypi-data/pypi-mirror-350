from enum import Enum


class PublishSchemaDtoDbColumnType(str, Enum):
    NUMERICAL = "NUMERICAL"
    TEXT = "TEXT"

    def __str__(self) -> str:
        return str(self.value)
