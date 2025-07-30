from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.stored_file_dto import StoredFileDto


T = TypeVar("T", bound="StreamDto")


@_attrs_define
class StreamDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        description (Union[Unset, str]):
        active (Union[Unset, bool]):
        creation_date (Union[Unset, int]):
        update_date (Union[Unset, int]):
        attachments (Union[Unset, List['StoredFileDto']]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    creation_date: Union[Unset, int] = UNSET
    update_date: Union[Unset, int] = UNSET
    attachments: Union[Unset, List["StoredFileDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        description = self.description

        active = self.active

        creation_date = self.creation_date

        update_date = self.update_date

        attachments: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if active is not UNSET:
            field_dict["active"] = active
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date
        if attachments is not UNSET:
            field_dict["attachments"] = attachments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.stored_file_dto import StoredFileDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        active = d.pop("active", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        update_date = d.pop("updateDate", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = StoredFileDto.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        stream_dto = cls(
            name=name,
            id=id,
            description=description,
            active=active,
            creation_date=creation_date,
            update_date=update_date,
            attachments=attachments,
        )

        stream_dto.additional_properties = d
        return stream_dto

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
