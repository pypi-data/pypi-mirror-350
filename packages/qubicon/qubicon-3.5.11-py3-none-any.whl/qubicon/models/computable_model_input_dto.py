from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto


T = TypeVar("T", bound="ComputableModelInputDto")


@_attrs_define
class ComputableModelInputDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        order (Union[Unset, int]):
        physical_quantity_unit (Union[Unset, PhysicalQuantityUnitDto]):
        description (Union[Unset, str]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    order: Union[Unset, int] = UNSET
    physical_quantity_unit: Union[Unset, "PhysicalQuantityUnitDto"] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        order = self.order

        physical_quantity_unit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.physical_quantity_unit, Unset):
            physical_quantity_unit = self.physical_quantity_unit.to_dict()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if order is not UNSET:
            field_dict["order"] = order
        if physical_quantity_unit is not UNSET:
            field_dict["physicalQuantityUnit"] = physical_quantity_unit
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        order = d.pop("order", UNSET)

        _physical_quantity_unit = d.pop("physicalQuantityUnit", UNSET)
        physical_quantity_unit: Union[Unset, PhysicalQuantityUnitDto]
        if isinstance(_physical_quantity_unit, Unset):
            physical_quantity_unit = UNSET
        else:
            physical_quantity_unit = PhysicalQuantityUnitDto.from_dict(_physical_quantity_unit)

        description = d.pop("description", UNSET)

        computable_model_input_dto = cls(
            name=name,
            id=id,
            order=order,
            physical_quantity_unit=physical_quantity_unit,
            description=description,
        )

        computable_model_input_dto.additional_properties = d
        return computable_model_input_dto

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
