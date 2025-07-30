from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.abstract_import_file_mapping_dto_type import AbstractImportFileMappingDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.any_import_file_mapping_column_dto import AnyImportFileMappingColumnDto


T = TypeVar("T", bound="OsmometerImportFileMappingDto")


@_attrs_define
class OsmometerImportFileMappingDto:
    """
    Attributes:
        type (Union[Unset, AbstractImportFileMappingDtoType]):
        columns (Union[Unset, List['AnyImportFileMappingColumnDto']]):
        sample_id_column (Union[Unset, int]):
        data_row (Union[Unset, int]):
    """

    type: Union[Unset, AbstractImportFileMappingDtoType] = UNSET
    columns: Union[Unset, List["AnyImportFileMappingColumnDto"]] = UNSET
    sample_id_column: Union[Unset, int] = UNSET
    data_row: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        columns: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        sample_id_column = self.sample_id_column

        data_row = self.data_row

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if columns is not UNSET:
            field_dict["columns"] = columns
        if sample_id_column is not UNSET:
            field_dict["sampleIdColumn"] = sample_id_column
        if data_row is not UNSET:
            field_dict["dataRow"] = data_row

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.any_import_file_mapping_column_dto import AnyImportFileMappingColumnDto

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, AbstractImportFileMappingDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AbstractImportFileMappingDtoType(_type)

        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = AnyImportFileMappingColumnDto.from_dict(columns_item_data)

            columns.append(columns_item)

        sample_id_column = d.pop("sampleIdColumn", UNSET)

        data_row = d.pop("dataRow", UNSET)

        osmometer_import_file_mapping_dto = cls(
            type=type,
            columns=columns,
            sample_id_column=sample_id_column,
            data_row=data_row,
        )

        osmometer_import_file_mapping_dto.additional_properties = d
        return osmometer_import_file_mapping_dto

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
