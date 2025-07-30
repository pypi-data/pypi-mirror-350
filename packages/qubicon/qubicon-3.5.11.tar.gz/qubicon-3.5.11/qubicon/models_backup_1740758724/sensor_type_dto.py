from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="SensorTypeDto")


@_attrs_define
class SensorTypeDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        creation_date (Union[Unset, int]):
        update_date (Union[Unset, int]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    creation_date: Union[Unset, int] = UNSET
    update_date: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        creation_date = self.creation_date

        update_date = self.update_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        update_date = d.pop("updateDate", UNSET)

        sensor_type_dto = cls(
            name=name,
            id=id,
            creation_date=creation_date,
            update_date=update_date,
        )

        sensor_type_dto.additional_properties = d
        return sensor_type_dto

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
