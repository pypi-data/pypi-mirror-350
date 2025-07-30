from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_annotations_item import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleAnnotationsItem,
    )
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_declared_annotations_item import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDeclaredAnnotationsItem,
    )
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_descriptor import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor,
    )
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_layer import (
        XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer,
    )


T = TypeVar("T", bound="XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModule")


@_attrs_define
class XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModule:
    """
    Attributes:
        layer (Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer]):
        name (Union[Unset, str]):
        descriptor (Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor]):
        named (Union[Unset, bool]):
        packages (Union[Unset, List[str]]):
        annotations (Union[Unset,
            List['XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleAnnotationsItem']]):
        declared_annotations (Union[Unset,
            List['XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDeclaredAnnotationsItem']]):
    """

    layer: Union[Unset, "XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer"] = UNSET
    name: Union[Unset, str] = UNSET
    descriptor: Union[Unset, "XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor"] = (
        UNSET
    )
    named: Union[Unset, bool] = UNSET
    packages: Union[Unset, List[str]] = UNSET
    annotations: Union[
        Unset, List["XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleAnnotationsItem"]
    ] = UNSET
    declared_annotations: Union[
        Unset, List["XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDeclaredAnnotationsItem"]
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        layer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.layer, Unset):
            layer = self.layer.to_dict()

        name = self.name

        descriptor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.descriptor, Unset):
            descriptor = self.descriptor.to_dict()

        named = self.named

        packages: Union[Unset, List[str]] = UNSET
        if not isinstance(self.packages, Unset):
            packages = self.packages

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
        if layer is not UNSET:
            field_dict["layer"] = layer
        if name is not UNSET:
            field_dict["name"] = name
        if descriptor is not UNSET:
            field_dict["descriptor"] = descriptor
        if named is not UNSET:
            field_dict["named"] = named
        if packages is not UNSET:
            field_dict["packages"] = packages
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if declared_annotations is not UNSET:
            field_dict["declaredAnnotations"] = declared_annotations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_annotations_item import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleAnnotationsItem,
        )
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_declared_annotations_item import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDeclaredAnnotationsItem,
        )
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_descriptor import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor,
        )
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module_layer import (
            XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer,
        )

        d = src_dict.copy()
        _layer = d.pop("layer", UNSET)
        layer: Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer]
        if isinstance(_layer, Unset):
            layer = UNSET
        else:
            layer = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleLayer.from_dict(_layer)

        name = d.pop("name", UNSET)

        _descriptor = d.pop("descriptor", UNSET)
        descriptor: Union[Unset, XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor]
        if isinstance(_descriptor, Unset):
            descriptor = UNSET
        else:
            descriptor = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDescriptor.from_dict(
                _descriptor
            )

        named = d.pop("named", UNSET)

        packages = cast(List[str], d.pop("packages", UNSET))

        annotations = []
        _annotations = d.pop("annotations", UNSET)
        for annotations_item_data in _annotations or []:
            annotations_item = (
                XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleAnnotationsItem.from_dict(
                    annotations_item_data
                )
            )

            annotations.append(annotations_item)

        declared_annotations = []
        _declared_annotations = d.pop("declaredAnnotations", UNSET)
        for declared_annotations_item_data in _declared_annotations or []:
            declared_annotations_item = XlsxParsingErrorModelThrowableStackTraceItemIncludeInfoFlagsUnnamedModuleDeclaredAnnotationsItem.from_dict(
                declared_annotations_item_data
            )

            declared_annotations.append(declared_annotations_item)

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module = cls(
            layer=layer,
            name=name,
            descriptor=descriptor,
            named=named,
            packages=packages,
            annotations=annotations,
            declared_annotations=declared_annotations,
        )

        xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module.additional_properties = d
        return xlsx_parsing_error_model_throwable_stack_trace_item_include_info_flags_unnamed_module

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
