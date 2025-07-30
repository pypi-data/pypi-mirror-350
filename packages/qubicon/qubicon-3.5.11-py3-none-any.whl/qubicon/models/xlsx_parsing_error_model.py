from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model_throwable import XlsxParsingErrorModelThrowable


T = TypeVar("T", bound="XlsxParsingErrorModel")


@_attrs_define
class XlsxParsingErrorModel:
    """
    Attributes:
        sheet_name (Union[Unset, str]):
        row_number (Union[Unset, int]):
        col_number (Union[Unset, int]):
        error_message (Union[Unset, str]):
        args (Union[Unset, List[str]]):
        throwable (Union[Unset, XlsxParsingErrorModelThrowable]):
    """

    sheet_name: Union[Unset, str] = UNSET
    row_number: Union[Unset, int] = UNSET
    col_number: Union[Unset, int] = UNSET
    error_message: Union[Unset, str] = UNSET
    args: Union[Unset, List[str]] = UNSET
    throwable: Union[Unset, "XlsxParsingErrorModelThrowable"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sheet_name = self.sheet_name

        row_number = self.row_number

        col_number = self.col_number

        error_message = self.error_message

        args: Union[Unset, List[str]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        throwable: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.throwable, Unset):
            throwable = self.throwable.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sheet_name is not UNSET:
            field_dict["sheetName"] = sheet_name
        if row_number is not UNSET:
            field_dict["rowNumber"] = row_number
        if col_number is not UNSET:
            field_dict["colNumber"] = col_number
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if args is not UNSET:
            field_dict["args"] = args
        if throwable is not UNSET:
            field_dict["throwable"] = throwable

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model_throwable import XlsxParsingErrorModelThrowable

        d = src_dict.copy()
        sheet_name = d.pop("sheetName", UNSET)

        row_number = d.pop("rowNumber", UNSET)

        col_number = d.pop("colNumber", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        args = cast(List[str], d.pop("args", UNSET))

        _throwable = d.pop("throwable", UNSET)
        throwable: Union[Unset, XlsxParsingErrorModelThrowable]
        if isinstance(_throwable, Unset):
            throwable = UNSET
        else:
            throwable = XlsxParsingErrorModelThrowable.from_dict(_throwable)

        xlsx_parsing_error_model = cls(
            sheet_name=sheet_name,
            row_number=row_number,
            col_number=col_number,
            error_message=error_message,
            args=args,
            throwable=throwable,
        )

        xlsx_parsing_error_model.additional_properties = d
        return xlsx_parsing_error_model

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
