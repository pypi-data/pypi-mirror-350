from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="StoredFileDto")


@_attrs_define
class StoredFileDto:
    """
    Attributes:
        file_uuid (str):
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        creation_date (Union[Unset, int]):
        update_date (Union[Unset, int]):
    """

    file_uuid: str
    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    creation_date: Union[Unset, int] = UNSET
    update_date: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_uuid = self.file_uuid

        id = self.id

        name = self.name

        creation_date = self.creation_date

        update_date = self.update_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileUUID": file_uuid,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_uuid = d.pop("fileUUID")

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        update_date = d.pop("updateDate", UNSET)

        stored_file_dto = cls(
            file_uuid=file_uuid,
            id=id,
            name=name,
            creation_date=creation_date,
            update_date=update_date,
        )

        stored_file_dto.additional_properties = d
        return stored_file_dto

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
