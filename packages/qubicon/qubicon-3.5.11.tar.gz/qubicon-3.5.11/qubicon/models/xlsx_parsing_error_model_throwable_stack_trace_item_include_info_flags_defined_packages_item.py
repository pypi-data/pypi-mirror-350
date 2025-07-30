from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item_annotations_item import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemAnnotationsItem,
    )
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item_declared_annotations_item import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemDeclaredAnnotationsItem,
    )


T = TypeVar("T", bound="XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItem")


@_attrs_define
class XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItem:
    """
    Attributes:
        name (Union[Unset, str]):
        specification_title (Union[Unset, str]):
        specification_version (Union[Unset, str]):
        specification_vendor (Union[Unset, str]):
        implementation_title (Union[Unset, str]):
        implementation_version (Union[Unset, str]):
        implementation_vendor (Union[Unset, str]):
        sealed (Union[Unset, bool]):
        annotations (Union[Unset,
            List['XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemAnnotationsItem']]):
        declared_annotations (Union[Unset, List['XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPack
            agesItemDeclaredAnnotationsItem']]):
    """

    name: Union[Unset, str] = UNSET
    specification_title: Union[Unset, str] = UNSET
    specification_version: Union[Unset, str] = UNSET
    specification_vendor: Union[Unset, str] = UNSET
    implementation_title: Union[Unset, str] = UNSET
    implementation_version: Union[Unset, str] = UNSET
    implementation_vendor: Union[Unset, str] = UNSET
    sealed: Union[Unset, bool] = UNSET
    annotations: Union[
        Unset, List["XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemAnnotationsItem"]
    ] = UNSET
    declared_annotations: Union[
        Unset,
        List["XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemDeclaredAnnotationsItem"],
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        specification_title = self.specification_title

        specification_version = self.specification_version

        specification_vendor = self.specification_vendor

        implementation_title = self.implementation_title

        implementation_version = self.implementation_version

        implementation_vendor = self.implementation_vendor

        sealed = self.sealed

        annotations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = []
            for annotations_item_data in self.annotations:
                annotations_item = annotations_item_data.to_dict()
                annotations.append(annotations_item)

        declared_annotations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.declared_annotations, Unset):
            declared_annotations = []
            for declared_annotations_item_data in self.declared_annotations:
                declared_annotations_item = declared_annotations_item_data.to_dict()
                declared_annotations.append(declared_annotations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if specification_title is not UNSET:
            field_dict["specificationTitle"] = specification_title
        if specification_version is not UNSET:
            field_dict["specificationVersion"] = specification_version
        if specification_vendor is not UNSET:
            field_dict["specificationVendor"] = specification_vendor
        if implementation_title is not UNSET:
            field_dict["implementationTitle"] = implementation_title
        if implementation_version is not UNSET:
            field_dict["implementationVersion"] = implementation_version
        if implementation_vendor is not UNSET:
            field_dict["implementationVendor"] = implementation_vendor
        if sealed is not UNSET:
            field_dict["sealed"] = sealed
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if declared_annotations is not UNSET:
            field_dict["declaredAnnotations"] = declared_annotations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item_annotations_item import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemAnnotationsItem,
        )
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item_declared_annotations_item import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemDeclaredAnnotationsItem,
        )

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        specification_title = d.pop("specificationTitle", UNSET)

        specification_version = d.pop("specificationVersion", UNSET)

        specification_vendor = d.pop("specificationVendor", UNSET)

        implementation_title = d.pop("implementationTitle", UNSET)

        implementation_version = d.pop("implementationVersion", UNSET)

        implementation_vendor = d.pop("implementationVendor", UNSET)

        sealed = d.pop("sealed", UNSET)

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemAnnotationsItem.from_dict(
                annotations_item_data
            )

            annotations.append(annotations_item)

        declared_annotations = []
        _declared_annotations = d.pop("declaredAnnotations", UNSET)
        for declared_annotations_item_data in _declared_annotations or []:
            declared_annotations_item = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsDefinedPackagesItemDeclaredAnnotationsItem.from_dict(
                declared_annotations_item_data
            )

            declared_annotations.append(declared_annotations_item)

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item = cls(
            name=name,
            specification_title=specification_title,
            specification_version=specification_version,
            specification_vendor=specification_vendor,
            implementation_title=implementation_title,
            implementation_version=implementation_version,
            implementation_vendor=implementation_vendor,
            sealed=sealed,
            annotations=annotations,
            declared_annotations=declared_annotations,
        )

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item.additional_properties = d
        return xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_defined_packages_item

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
