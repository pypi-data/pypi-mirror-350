from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags,
    )


T = TypeVar("T", bound="XlsxParsingErrorModelThrowableStackTraceItem")


@_attrs_define
class XlsxParsingErrorModelThrowableStackTraceItem:
    """
    Attributes:
        module_name (Union[Unset, str]):
        module_version (Union[Unset, str]):
        class_loader_name (Union[Unset, str]):
        method_name (Union[Unset, str]):
        file_name (Union[Unset, str]):
        line_number (Union[Unset, int]):
        include_info_flags (Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags]):
        class_name (Union[Unset, str]):
        native_method (Union[Unset, bool]):
    """

    module_name: Union[Unset, str] = UNSET
    module_version: Union[Unset, str] = UNSET
    class_loader_name: Union[Unset, str] = UNSET
    method_name: Union[Unset, str] = UNSET
    file_name: Union[Unset, str] = UNSET
    line_number: Union[Unset, int] = UNSET
    include_info_flags: Union[Unset, "XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags"] = UNSET
    class_name: Union[Unset, str] = UNSET
    native_method: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        module_name = self.module_name

        module_version = self.module_version

        class_loader_name = self.class_loader_name

        method_name = self.method_name

        file_name = self.file_name

        line_number = self.line_number

        include_info_flags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.include_info_flags, Unset):
            include_info_flags = self.include_info_flags.to_dict()

        class_name = self.class_name

        native_method = self.native_method

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if module_name is not UNSET:
            field_dict["moduleName"] = module_name
        if module_version is not UNSET:
            field_dict["moduleVersion"] = module_version
        if class_loader_name is not UNSET:
            field_dict["classLoaderName"] = class_loader_name
        if method_name is not UNSET:
            field_dict["methodName"] = method_name
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if line_number is not UNSET:
            field_dict["lineNumber"] = line_number
        if include_info_flags is not UNSET:
            field_dict["includeInfoFlags"] = include_info_flags
        if class_name is not UNSET:
            field_dict["className"] = class_name
        if native_method is not UNSET:
            field_dict["nativeMethod"] = native_method

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags,
        )

        d = src_dict.copy()
        module_name = d.pop("moduleName", UNSET)

        module_version = d.pop("moduleVersion", UNSET)

        class_loader_name = d.pop("classLoaderName", UNSET)

        method_name = d.pop("methodName", UNSET)

        file_name = d.pop("fileName", UNSET)

        line_number = d.pop("lineNumber", UNSET)

        _include_info_flags = d.pop("includeInfoFlags", UNSET)
        include_info_flags: Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags]
        if isinstance(_include_info_flags, Unset):
            include_info_flags = UNSET
        else:
            include_info_flags = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlags.from_dict(
                _include_info_flags
            )

        class_name = d.pop("className", UNSET)

        native_method = d.pop("nativeMethod", UNSET)

        xlsx_parsing_error_model_throwable_stack_trace_item = cls(
            module_name=module_name,
            module_version=module_version,
            class_loader_name=class_loader_name,
            method_name=method_name,
            file_name=file_name,
            line_number=line_number,
            include_info_flags=include_info_flags,
            class_name=class_name,
            native_method=native_method,
        )

        xlsx_parsing_error_model_throwable_stack_trace_item.additional_properties = d
        return xlsx_parsing_error_model_throwable_stack_trace_item

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
