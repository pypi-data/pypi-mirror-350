from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor")


@_attrs_define
class XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor:
    """
    Attributes:
        open_ (Union[Unset, bool]):
        automatic (Union[Unset, bool]):
    """

    open_: Union[Unset, bool] = UNSET
    automatic: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        open_ = self.open_

        automatic = self.automatic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if open_ is not UNSET:
            field_dict["open"] = open_
        if automatic is not UNSET:
            field_dict["automatic"] = automatic

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        open_ = d.pop("open", UNSET)

        automatic = d.pop("automatic", UNSET)

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_descriptor = cls(
            open_=open_,
            automatic=automatic,
        )

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_descriptor.additional_properties = d
        return xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_descriptor

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
