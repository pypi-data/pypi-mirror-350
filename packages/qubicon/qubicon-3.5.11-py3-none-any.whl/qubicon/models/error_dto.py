from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multi_language_label_dto import MultiLanguageLabelDto


T = TypeVar("T", bound="ErrorDto")


@_attrs_define
class ErrorDto:
    """
    Attributes:
        trace (Union[Unset, str]):
        message (Union[Unset, str]):
        multi_language_label (Union[Unset, MultiLanguageLabelDto]):
        reasons (Union[Unset, List['ErrorDto']]):
    """

    trace: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    multi_language_label: Union[Unset, "MultiLanguageLabelDto"] = UNSET
    reasons: Union[Unset, List["ErrorDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trace = self.trace

        message = self.message

        multi_language_label: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.multi_language_label, Unset):
            multi_language_label = self.multi_language_label.to_dict()

        reasons: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.reasons, Unset):
            reasons = []
            for reasons_item_data in self.reasons:
                reasons_item = reasons_item_data.to_dict()
                reasons.append(reasons_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if trace is not UNSET:
            field_dict["trace"] = trace
        if message is not UNSET:
            field_dict["message"] = message
        if multi_language_label is not UNSET:
            field_dict["multiLanguageLabel"] = multi_language_label
        if reasons is not UNSET:
            field_dict["reasons"] = reasons

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.multi_language_label_dto import MultiLanguageLabelDto

        d = src_dict.copy()
        trace = d.pop("trace", UNSET)

        message = d.pop("message", UNSET)

        _multi_language_label = d.pop("multiLanguageLabel", UNSET)
        multi_language_label: Union[Unset, MultiLanguageLabelDto]
        if isinstance(_multi_language_label, Unset):
            multi_language_label = UNSET
        else:
            multi_language_label = MultiLanguageLabelDto.from_dict(_multi_language_label)

        reasons = []
        _reasons = d.pop("reasons", UNSET)
        for reasons_item_data in _reasons or []:
            reasons_item = ErrorDto.from_dict(reasons_item_data)

            reasons.append(reasons_item)

        error_dto = cls(
            trace=trace,
            message=message,
            multi_language_label=multi_language_label,
            reasons=reasons,
        )

        error_dto.additional_properties = d
        return error_dto

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
