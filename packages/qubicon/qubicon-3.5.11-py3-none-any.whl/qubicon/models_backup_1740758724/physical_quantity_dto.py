from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.physical_quantity_dto_status import PhysicalQuantityDtoStatus
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto


T = TypeVar("T", bound="PhysicalQuantityDto")


@_attrs_define
class PhysicalQuantityDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        status (Union[Unset, PhysicalQuantityDtoStatus]):
        units (Union[Unset, List['PhysicalQuantityUnitDto']]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    status: Union[Unset, PhysicalQuantityDtoStatus] = UNSET
    units: Union[Unset, List["PhysicalQuantityUnitDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        units: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.units, Unset):
            units = []
            for units_item_data in self.units:
                units_item = units_item_data.to_dict()
                units.append(units_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, PhysicalQuantityDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PhysicalQuantityDtoStatus(_status)

        units = []
        _units = d.pop("units", UNSET)
        for units_item_data in _units or []:
            units_item = PhysicalQuantityUnitDto.from_dict(units_item_data)

            units.append(units_item)

        physical_quantity_dto = cls(
            name=name,
            id=id,
            status=status,
            units=units,
        )

        physical_quantity_dto.additional_properties = d
        return physical_quantity_dto

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
