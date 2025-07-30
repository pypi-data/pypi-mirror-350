from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.external_python_computable_model_dto import ExternalPythonComputableModelDto
    from ..models.jython_computable_model_dto import JythonComputableModelDto
    from ..models.page_meta_data_dto import PageMetaDataDto


T = TypeVar("T", bound="PageDtoAbstractComputableModelDto")


@_attrs_define
class PageDtoAbstractComputableModelDto:
    """
    Attributes:
        content (Union[Unset, List[Union['ExternalPythonComputableModelDto', 'JythonComputableModelDto']]]):
        page (Union[Unset, PageMetaDataDto]):
    """

    content: Union[Unset, List[Union["ExternalPythonComputableModelDto", "JythonComputableModelDto"]]] = UNSET
    page: Union[Unset, "PageMetaDataDto"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.external_python_computable_model_dto import ExternalPythonComputableModelDto

        content: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item: Dict[str, Any]
                if isinstance(content_item_data, ExternalPythonComputableModelDto):
                    content_item = content_item_data.to_dict()
                else:
                    content_item = content_item_data.to_dict()

                content.append(content_item)

        page: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.page, Unset):
            page = self.page.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if content is not UNSET:
            field_dict["content"] = content
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_python_computable_model_dto import ExternalPythonComputableModelDto
        from ..models.jython_computable_model_dto import JythonComputableModelDto
        from ..models.page_meta_data_dto import PageMetaDataDto

        d = src_dict.copy()
        content = []
        _content = d.pop("content", UNSET)
        for content_item_data in _content or []:

            def _parse_content_item(
                data: object,
            ) -> Union["ExternalPythonComputableModelDto", "JythonComputableModelDto"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    content_item_type_0 = ExternalPythonComputableModelDto.from_dict(data)

                    return content_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                content_item_type_1 = JythonComputableModelDto.from_dict(data)

                return content_item_type_1

            content_item = _parse_content_item(content_item_data)

            content.append(content_item)

        _page = d.pop("page", UNSET)
        page: Union[Unset, PageMetaDataDto]
        if isinstance(_page, Unset):
            page = UNSET
        else:
            page = PageMetaDataDto.from_dict(_page)

        page_dto_abstract_computable_model_dto = cls(
            content=content,
            page=page,
        )

        page_dto_abstract_computable_model_dto.additional_properties = d
        return page_dto_abstract_computable_model_dto

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
