from enum import Enum


class DirectToProcessImportFileProgressType(str, Enum):
    CEDEX = "Cedex"
    DIRECTIMPORT = "DirectImport"
    GASCHROMATOGRAPHY = "GasChromatography"
    NANODROP = "NanoDrop"
    OSMOMETER = "Osmometer"
    PHMETER = "PHMeter"
    PHOTOMETER = "PhotoMeter"
    SDC = "Sdc"
    VICELL = "ViCell"

    def __str__(self) -> str:
        return str(self.value)
