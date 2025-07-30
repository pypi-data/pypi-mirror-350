from enum import Enum


class ProcessDtoProcessArchiveTransitionStatus(str, Enum):
    ARCHIVED = "ARCHIVED"
    ARCHIVE_IN_PROGRESS = "ARCHIVE_IN_PROGRESS"
    ARCHIVE_MANUALLY_SCHEDULED = "ARCHIVE_MANUALLY_SCHEDULED"
    UNARCHIVED_MANUALLY = "UNARCHIVED_MANUALLY"
    UNARCHIVE_IN_PROGRESS = "UNARCHIVE_IN_PROGRESS"
    UNTOUCHED = "UNTOUCHED"

    def __str__(self) -> str:
        return str(self.value)
