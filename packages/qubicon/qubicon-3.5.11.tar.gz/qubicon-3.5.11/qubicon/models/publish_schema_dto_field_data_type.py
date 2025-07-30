from enum import Enum


class PublishSchemaDtoFieldDataType(str, Enum):
    EXTERNAL = "EXTERNAL"
    MATERIAL = "MATERIAL"
    MATERIAL_LOT = "MATERIAL_LOT"
    METADATA = "METADATA"
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"
    ORGANISM = "ORGANISM"
    ORGANISM_VIAL = "ORGANISM_VIAL"
    SOFT_SENSOR = "SOFT_SENSOR"
    TAG_MULTIPLE = "TAG_MULTIPLE"
    TAG_SINGLE = "TAG_SINGLE"

    def __str__(self) -> str:
        return str(self.value)
