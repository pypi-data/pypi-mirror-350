from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable_stack_trace_item import (
        XlsxParsingErrorModelThrowableStackTraceItem,
    )


T = TypeVar("T", bound="XlsxParsingErrorModelThrowable")


@_attrs_define
class XlsxParsingErrorModelThrowable:
    """
    Attributes:
        stack_trace (Union[Unset, List['XlsxParsingErrorModelThrowableStackTraceItem']]):
        message (Union[Unset, str]):
        localized_message (Union[Unset, str]):
    """

    stack_trace: Union[Unset, List["XlsxParsingErrorModelThrowableStackTraceItem"]] = UNSET
    message: Union[Unset, str] = UNSET
    localized_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        stack_trace: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.stack_trace, Unset):
            stack_trace = []
            for stack_trace_item_data in self.stack_trace:
                stack_trace_item = stack_trace_item_data.to_dict()
                stack_trace.append(stack_trace_item)

        message = self.message

        localized_message = self.localized_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if stack_trace is not UNSET:
            field_dict["stackTrace"] = stack_trace
        if message is not UNSET:
            field_dict["message"] = message
        if localized_message is not UNSET:
            field_dict["localizedMessage"] = localized_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable_stack_trace_item import (
            XlsxParsingErrorModelThrowableStackTraceItem,
        )

        d = src_dict.copy()
        stack_trace = []
        _stack_trace = d.pop("stackTrace", UNSET)
        for stack_trace_item_data in _stack_trace or []:
            stack_trace_item = XlsxParsingErrorModelThrowableStackTraceItem.from_dict(stack_trace_item_data)

            stack_trace.append(stack_trace_item)

        message = d.pop("message", UNSET)

        localized_message = d.pop("localizedMessage", UNSET)

        xlsx_parsing_error_model_throwable = cls(
            stack_trace=stack_trace,
            message=message,
            localized_message=localized_message,
        )

        xlsx_parsing_error_model_throwable.additional_properties = d
        return xlsx_parsing_error_model_throwable

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
