from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent_defined_packages_item import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentDefinedPackagesItem,
    )
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent_unnamed_module import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule,
    )


T = TypeVar("T", bound="XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParent")


@_attrs_define
class XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParent:
    """
    Attributes:
        unnamed_module (Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule]):
        default_assertion_status (Union[Unset, bool]):
        name (Union[Unset, str]):
        defined_packages (Union[Unset,
            List['XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentDefinedPackagesItem']]):
        default_assertion_status_impl (Union[Unset, bool]):
        registered_as_parallel_capable (Union[Unset, bool]):
    """

    unnamed_module: Union[Unset, "XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule"] = (
        UNSET
    )
    default_assertion_status: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    defined_packages: Union[
        Unset, List["XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentDefinedPackagesItem"]
    ] = UNSET
    default_assertion_status_impl: Union[Unset, bool] = UNSET
    registered_as_parallel_capable: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unnamed_module: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.unnamed_module, Unset):
            unnamed_module = self.unnamed_module.to_dict()

        default_assertion_status = self.default_assertion_status

        name = self.name

        defined_packages: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.defined_packages, Unset):
            defined_packages = []
            for defined_packages_item_data in self.defined_packages:
                defined_packages_item = defined_packages_item_data.to_dict()
                defined_packages.append(defined_packages_item)

        default_assertion_status_impl = self.default_assertion_status_impl

        registered_as_parallel_capable = self.registered_as_parallel_capable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if unnamed_module is not UNSET:
            field_dict["unnamedModule"] = unnamed_module
        if default_assertion_status is not UNSET:
            field_dict["defaultAssertionStatus"] = default_assertion_status
        if name is not UNSET:
            field_dict["name"] = name
        if defined_packages is not UNSET:
            field_dict["definedPackages"] = defined_packages
        if default_assertion_status_impl is not UNSET:
            field_dict["defaultAssertionStatusImpl"] = default_assertion_status_impl
        if registered_as_parallel_capable is not UNSET:
            field_dict["registeredAsParallelCapable"] = registered_as_parallel_capable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent_defined_packages_item import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentDefinedPackagesItem,
        )
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent_unnamed_module import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule,
        )

        d = src_dict.copy()
        _unnamed_module = d.pop("unnamedModule", UNSET)
        unnamed_module: Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule]
        if isinstance(_unnamed_module, Unset):
            unnamed_module = UNSET
        else:
            unnamed_module = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentUnnamedModule.from_dict(
                _unnamed_module
            )

        default_assertion_status = d.pop("defaultAssertionStatus", UNSET)

        name = d.pop("name", UNSET)

        defined_packages = []
        _defined_packages = d.pop("definedPackages", UNSET)
        for defined_packages_item_data in _defined_packages or []:
            defined_packages_item = (
                XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsParentDefinedPackagesItem.from_dict(
                    defined_packages_item_data
                )
            )

            defined_packages.append(defined_packages_item)

        default_assertion_status_impl = d.pop("defaultAssertionStatusImpl", UNSET)

        registered_as_parallel_capable = d.pop("registeredAsParallelCapable", UNSET)

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent = cls(
            unnamed_module=unnamed_module,
            default_assertion_status=default_assertion_status,
            name=name,
            defined_packages=defined_packages,
            default_assertion_status_impl=default_assertion_status_impl,
            registered_as_parallel_capable=registered_as_parallel_capable,
        )

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent.additional_properties = d
        return xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_parent

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
