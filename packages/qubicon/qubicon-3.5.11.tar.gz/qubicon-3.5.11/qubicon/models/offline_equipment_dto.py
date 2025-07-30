from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offline_equipment_dto_status import OfflineEquipmentDtoStatus
from ..models.offline_equipment_dto_type import OfflineEquipmentDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.abstract_import_file_mapping_dto import AbstractImportFileMappingDto
    from ..models.ce_dex_import_file_mapping_dto import CeDexImportFileMappingDto
    from ..models.gmp_track_dto import GmpTrackDto
    from ..models.nano_drop_import_file_mapping_dto import NanoDropImportFileMappingDto
    from ..models.osmometer_import_file_mapping_dto import OsmometerImportFileMappingDto
    from ..models.ph_meter_import_file_mapping_dto import PHMeterImportFileMappingDto
    from ..models.photo_meter_import_file_mapping_dto import PhotoMeterImportFileMappingDto
    from ..models.vi_cell_import_file_mapping_dto import ViCellImportFileMappingDto


T = TypeVar("T", bound="OfflineEquipmentDto")


@_attrs_define
class OfflineEquipmentDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        type (Union[Unset, OfflineEquipmentDtoType]):
        status (Union[Unset, OfflineEquipmentDtoStatus]):
        gmp_enabled (Union[Unset, bool]):
        gmp_track (Union[Unset, GmpTrackDto]):
        deleted (Union[Unset, bool]):
        mapping_imported (Union[Unset, bool]):
        mapping (Union['AbstractImportFileMappingDto', 'CeDexImportFileMappingDto', 'NanoDropImportFileMappingDto',
            'OsmometerImportFileMappingDto', 'PHMeterImportFileMappingDto', 'PhotoMeterImportFileMappingDto',
            'ViCellImportFileMappingDto', Unset]):
        automatic_folder_name (Union[Unset, str]):
        version_group_first_id (Union[Unset, int]):
        version_group_copied_from_id (Union[Unset, int]):
        version_group_version (Union[Unset, int]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    type: Union[Unset, OfflineEquipmentDtoType] = UNSET
    status: Union[Unset, OfflineEquipmentDtoStatus] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    gmp_track: Union[Unset, "GmpTrackDto"] = UNSET
    deleted: Union[Unset, bool] = UNSET
    mapping_imported: Union[Unset, bool] = UNSET
    mapping: Union[
        "AbstractImportFileMappingDto",
        "CeDexImportFileMappingDto",
        "NanoDropImportFileMappingDto",
        "OsmometerImportFileMappingDto",
        "PHMeterImportFileMappingDto",
        "PhotoMeterImportFileMappingDto",
        "ViCellImportFileMappingDto",
        Unset,
    ] = UNSET
    automatic_folder_name: Union[Unset, str] = UNSET
    version_group_first_id: Union[Unset, int] = UNSET
    version_group_copied_from_id: Union[Unset, int] = UNSET
    version_group_version: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.abstract_import_file_mapping_dto import AbstractImportFileMappingDto
        from ..models.ce_dex_import_file_mapping_dto import CeDexImportFileMappingDto
        from ..models.nano_drop_import_file_mapping_dto import NanoDropImportFileMappingDto
        from ..models.osmometer_import_file_mapping_dto import OsmometerImportFileMappingDto
        from ..models.ph_meter_import_file_mapping_dto import PHMeterImportFileMappingDto
        from ..models.photo_meter_import_file_mapping_dto import PhotoMeterImportFileMappingDto

        name = self.name

        id = self.id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        gmp_enabled = self.gmp_enabled

        gmp_track: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.gmp_track, Unset):
            gmp_track = self.gmp_track.to_dict()

        deleted = self.deleted

        mapping_imported = self.mapping_imported

        mapping: Union[Dict[str, Any], Unset]
        if isinstance(self.mapping, Unset):
            mapping = UNSET
        elif isinstance(self.mapping, AbstractImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, CeDexImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, AbstractImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, NanoDropImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, OsmometerImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, PHMeterImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, PhotoMeterImportFileMappingDto):
            mapping = self.mapping.to_dict()
        elif isinstance(self.mapping, AbstractImportFileMappingDto):
            mapping = self.mapping.to_dict()
        else:
            mapping = self.mapping.to_dict()

        automatic_folder_name = self.automatic_folder_name

        version_group_first_id = self.version_group_first_id

        version_group_copied_from_id = self.version_group_copied_from_id

        version_group_version = self.version_group_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if status is not UNSET:
            field_dict["status"] = status
        if gmp_enabled is not UNSET:
            field_dict["gmpEnabled"] = gmp_enabled
        if gmp_track is not UNSET:
            field_dict["gmpTrack"] = gmp_track
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if mapping_imported is not UNSET:
            field_dict["mappingImported"] = mapping_imported
        if mapping is not UNSET:
            field_dict["mapping"] = mapping
        if automatic_folder_name is not UNSET:
            field_dict["automaticFolderName"] = automatic_folder_name
        if version_group_first_id is not UNSET:
            field_dict["versionGroupFirstId"] = version_group_first_id
        if version_group_copied_from_id is not UNSET:
            field_dict["versionGroupCopiedFromId"] = version_group_copied_from_id
        if version_group_version is not UNSET:
            field_dict["versionGroupVersion"] = version_group_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.abstract_import_file_mapping_dto import AbstractImportFileMappingDto
        from ..models.ce_dex_import_file_mapping_dto import CeDexImportFileMappingDto
        from ..models.gmp_track_dto import GmpTrackDto
        from ..models.nano_drop_import_file_mapping_dto import NanoDropImportFileMappingDto
        from ..models.osmometer_import_file_mapping_dto import OsmometerImportFileMappingDto
        from ..models.ph_meter_import_file_mapping_dto import PHMeterImportFileMappingDto
        from ..models.photo_meter_import_file_mapping_dto import PhotoMeterImportFileMappingDto
        from ..models.vi_cell_import_file_mapping_dto import ViCellImportFileMappingDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, OfflineEquipmentDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = OfflineEquipmentDtoType(_type)

        _status = d.pop("status", UNSET)
        status: Union[Unset, OfflineEquipmentDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = OfflineEquipmentDtoStatus(_status)

        gmp_enabled = d.pop("gmpEnabled", UNSET)

        _gmp_track = d.pop("gmpTrack", UNSET)
        gmp_track: Union[Unset, GmpTrackDto]
        if isinstance(_gmp_track, Unset):
            gmp_track = UNSET
        else:
            gmp_track = GmpTrackDto.from_dict(_gmp_track)

        deleted = d.pop("deleted", UNSET)

        mapping_imported = d.pop("mappingImported", UNSET)

        def _parse_mapping(
            data: object,
        ) -> Union[
            "AbstractImportFileMappingDto",
            "CeDexImportFileMappingDto",
            "NanoDropImportFileMappingDto",
            "OsmometerImportFileMappingDto",
            "PHMeterImportFileMappingDto",
            "PhotoMeterImportFileMappingDto",
            "ViCellImportFileMappingDto",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_0 = AbstractImportFileMappingDto.from_dict(data)

                return mapping_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_1 = CeDexImportFileMappingDto.from_dict(data)

                return mapping_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_2 = AbstractImportFileMappingDto.from_dict(data)

                return mapping_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_3 = NanoDropImportFileMappingDto.from_dict(data)

                return mapping_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_4 = OsmometerImportFileMappingDto.from_dict(data)

                return mapping_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_5 = PHMeterImportFileMappingDto.from_dict(data)

                return mapping_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_6 = PhotoMeterImportFileMappingDto.from_dict(data)

                return mapping_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                mapping_type_7 = AbstractImportFileMappingDto.from_dict(data)

                return mapping_type_7
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            mapping_type_8 = ViCellImportFileMappingDto.from_dict(data)

            return mapping_type_8

        mapping = _parse_mapping(d.pop("mapping", UNSET))

        automatic_folder_name = d.pop("automaticFolderName", UNSET)

        version_group_first_id = d.pop("versionGroupFirstId", UNSET)

        version_group_copied_from_id = d.pop("versionGroupCopiedFromId", UNSET)

        version_group_version = d.pop("versionGroupVersion", UNSET)

        offline_equipment_dto = cls(
            name=name,
            id=id,
            type=type,
            status=status,
            gmp_enabled=gmp_enabled,
            gmp_track=gmp_track,
            deleted=deleted,
            mapping_imported=mapping_imported,
            mapping=mapping,
            automatic_folder_name=automatic_folder_name,
            version_group_first_id=version_group_first_id,
            version_group_copied_from_id=version_group_copied_from_id,
            version_group_version=version_group_version,
        )

        offline_equipment_dto.additional_properties = d
        return offline_equipment_dto

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
