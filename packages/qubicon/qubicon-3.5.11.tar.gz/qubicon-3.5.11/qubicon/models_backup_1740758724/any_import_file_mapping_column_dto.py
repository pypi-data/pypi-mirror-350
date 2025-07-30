from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto


T = TypeVar("T", bound="AnyImportFileMappingColumnDto")


@_attrs_define
class AnyImportFileMappingColumnDto:
    """
    Attributes:
        uid (Union[Unset, str]):
        column (Union[Unset, str]):
        gas_chromatography_file_extension (Union[Unset, str]):
        column_num (Union[Unset, int]):
        tag_name (Union[Unset, str]):
        qubicon_name (Union[Unset, str]):
        numerical (Union[Unset, bool]):
        favorite (Union[Unset, bool]):
        physical_quantity_unit (Union[Unset, PhysicalQuantityUnitDto]):
        multiplication_factor (Union[Unset, float]):
    """

    uid: Union[Unset, str] = UNSET
    column: Union[Unset, str] = UNSET
    gas_chromatography_file_extension: Union[Unset, str] = UNSET
    column_num: Union[Unset, int] = UNSET
    tag_name: Union[Unset, str] = UNSET
    qubicon_name: Union[Unset, str] = UNSET
    numerical: Union[Unset, bool] = UNSET
    favorite: Union[Unset, bool] = UNSET
    physical_quantity_unit: Union[Unset, "PhysicalQuantityUnitDto"] = UNSET
    multiplication_factor: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid

        column = self.column

        gas_chromatography_file_extension = self.gas_chromatography_file_extension

        column_num = self.column_num

        tag_name = self.tag_name

        qubicon_name = self.qubicon_name

        numerical = self.numerical

        favorite = self.favorite

        physical_quantity_unit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.physical_quantity_unit, Unset):
            physical_quantity_unit = self.physical_quantity_unit.to_dict()

        multiplication_factor = self.multiplication_factor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uid is not UNSET:
            field_dict["uid"] = uid
        if column is not UNSET:
            field_dict["column"] = column
        if gas_chromatography_file_extension is not UNSET:
            field_dict["gasChromatographyFileExtension"] = gas_chromatography_file_extension
        if column_num is not UNSET:
            field_dict["columnNum"] = column_num
        if tag_name is not UNSET:
            field_dict["tagName"] = tag_name
        if qubicon_name is not UNSET:
            field_dict["qubiconName"] = qubicon_name
        if numerical is not UNSET:
            field_dict["numerical"] = numerical
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if physical_quantity_unit is not UNSET:
            field_dict["physicalQuantityUnit"] = physical_quantity_unit
        if multiplication_factor is not UNSET:
            field_dict["multiplicationFactor"] = multiplication_factor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto

        d = src_dict.copy()
        uid = d.pop("uid", UNSET)

        column = d.pop("column", UNSET)

        gas_chromatography_file_extension = d.pop("gasChromatographyFileExtension", UNSET)

        column_num = d.pop("columnNum", UNSET)

        tag_name = d.pop("tagName", UNSET)

        qubicon_name = d.pop("qubiconName", UNSET)

        numerical = d.pop("numerical", UNSET)

        favorite = d.pop("favorite", UNSET)

        _physical_quantity_unit = d.pop("physicalQuantityUnit", UNSET)
        physical_quantity_unit: Union[Unset, PhysicalQuantityUnitDto]
        if isinstance(_physical_quantity_unit, Unset):
            physical_quantity_unit = UNSET
        else:
            physical_quantity_unit = PhysicalQuantityUnitDto.from_dict(_physical_quantity_unit)

        multiplication_factor = d.pop("multiplicationFactor", UNSET)

        any_import_file_mapping_column_dto = cls(
            uid=uid,
            column=column,
            gas_chromatography_file_extension=gas_chromatography_file_extension,
            column_num=column_num,
            tag_name=tag_name,
            qubicon_name=qubicon_name,
            numerical=numerical,
            favorite=favorite,
            physical_quantity_unit=physical_quantity_unit,
            multiplication_factor=multiplication_factor,
        )

        any_import_file_mapping_column_dto.additional_properties = d
        return any_import_file_mapping_column_dto

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
