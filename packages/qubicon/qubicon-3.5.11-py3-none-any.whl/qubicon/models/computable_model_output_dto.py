from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto
    from ..models.publish_schema_dto import PublishSchemaDto


T = TypeVar("T", bound="ComputableModelOutputDto")


@_attrs_define
class ComputableModelOutputDto:
    """
    Attributes:
        name (str):
        physical_quantity_unit (PhysicalQuantityUnitDto):
        id (Union[Unset, int]):
        description (Union[Unset, str]):
        publish_field (Union[Unset, PublishSchemaDto]):
        order (Union[Unset, int]):
    """

    name: str
    physical_quantity_unit: "PhysicalQuantityUnitDto"
    id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    publish_field: Union[Unset, "PublishSchemaDto"] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        physical_quantity_unit = self.physical_quantity_unit.to_dict()

        id = self.id

        description = self.description

        publish_field: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.publish_field, Unset):
            publish_field = self.publish_field.to_dict()

        order = self.order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "physicalQuantityUnit": physical_quantity_unit,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if publish_field is not UNSET:
            field_dict["publishField"] = publish_field
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto
        from ..models.publish_schema_dto import PublishSchemaDto

        d = src_dict.copy()
        name = d.pop("name")

        physical_quantity_unit = PhysicalQuantityUnitDto.from_dict(d.pop("physicalQuantityUnit"))

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        _publish_field = d.pop("publishField", UNSET)
        publish_field: Union[Unset, PublishSchemaDto]
        if isinstance(_publish_field, Unset):
            publish_field = UNSET
        else:
            publish_field = PublishSchemaDto.from_dict(_publish_field)

        order = d.pop("order", UNSET)

        computable_model_output_dto = cls(
            name=name,
            physical_quantity_unit=physical_quantity_unit,
            id=id,
            description=description,
            publish_field=publish_field,
            order=order,
        )

        computable_model_output_dto.additional_properties = d
        return computable_model_output_dto

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
