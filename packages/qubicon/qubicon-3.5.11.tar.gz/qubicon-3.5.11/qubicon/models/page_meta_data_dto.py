from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="PageMetaDataDto")


@_attrs_define
class PageMetaDataDto:
    """
    Attributes:
        size (Union[Unset, int]):
        page (Union[Unset, int]):
        pages (Union[Unset, int]):
        total_elements (Union[Unset, int]):
    """

    size: Union[Unset, int] = UNSET
    page: Union[Unset, int] = UNSET
    pages: Union[Unset, int] = UNSET
    total_elements: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        size = self.size

        page = self.page

        pages = self.pages

        total_elements = self.total_elements

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if page is not UNSET:
            field_dict["page"] = page
        if pages is not UNSET:
            field_dict["pages"] = pages
        if total_elements is not UNSET:
            field_dict["totalElements"] = total_elements

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        page = d.pop("page", UNSET)

        pages = d.pop("pages", UNSET)

        total_elements = d.pop("totalElements", UNSET)

        page_meta_data_dto = cls(
            size=size,
            page=page,
            pages=pages,
            total_elements=total_elements,
        )

        page_meta_data_dto.additional_properties = d
        return page_meta_data_dto

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
