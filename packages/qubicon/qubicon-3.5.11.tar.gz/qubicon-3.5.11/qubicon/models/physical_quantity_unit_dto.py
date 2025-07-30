from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.physical_quantity_unit_dto_status import PhysicalQuantityUnitDtoStatus
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="PhysicalQuantityUnitDto")


@_attrs_define
class PhysicalQuantityUnitDto:
    """
    Attributes:
        unit (str):
        name (str):
        id (Union[Unset, int]):
        physical_quantity_id (Union[Unset, int]):
        status (Union[Unset, PhysicalQuantityUnitDtoStatus]):
    """

    unit: str
    name: str
    id: Union[Unset, int] = UNSET
    physical_quantity_id: Union[Unset, int] = UNSET
    status: Union[Unset, PhysicalQuantityUnitDtoStatus] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unit = self.unit

        name = self.name

        id = self.id

        physical_quantity_id = self.physical_quantity_id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unit": unit,
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if physical_quantity_id is not UNSET:
            field_dict["physicalQuantityId"] = physical_quantity_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unit = d.pop("unit")

        name = d.pop("name")

        id = d.pop("id", UNSET)

        physical_quantity_id = d.pop("physicalQuantityId", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, PhysicalQuantityUnitDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = PhysicalQuantityUnitDtoStatus(_status)

        physical_quantity_unit_dto = cls(
            unit=unit,
            name=name,
            id=id,
            physical_quantity_id=physical_quantity_id,
            status=status,
        )

        physical_quantity_unit_dto.additional_properties = d
        return physical_quantity_unit_dto

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
