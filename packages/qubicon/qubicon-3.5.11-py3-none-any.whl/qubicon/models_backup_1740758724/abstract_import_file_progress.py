from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.abstract_import_file_progress_type import AbstractImportFileProgressType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.xlsx_parsing_error_model import XlsxParsingErrorModel


T = TypeVar("T", bound="AbstractImportFileProgress")


@_attrs_define
class AbstractImportFileProgress:
    """
    Attributes:
        grand_failure (Union[Unset, bool]):
        grand_skipped (Union[Unset, bool]):
        errors (Union[Unset, List['XlsxParsingErrorModel']]):
        type (Union[Unset, AbstractImportFileProgressType]):
        last_processed_record_number (Union[Unset, int]):
        total_rows (Union[Unset, int]):
        failed_rows (Union[Unset, int]):
        failed_cells_count (Union[Unset, int]):
        total_columns (Union[Unset, int]):
        existing_cells (Union[Unset, int]):
    """

    grand_failure: Union[Unset, bool] = UNSET
    grand_skipped: Union[Unset, bool] = UNSET
    errors: Union[Unset, List["XlsxParsingErrorModel"]] = UNSET
    type: Union[Unset, AbstractImportFileProgressType] = UNSET
    last_processed_record_number: Union[Unset, int] = UNSET
    total_rows: Union[Unset, int] = UNSET
    failed_rows: Union[Unset, int] = UNSET
    failed_cells_count: Union[Unset, int] = UNSET
    total_columns: Union[Unset, int] = UNSET
    existing_cells: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        grand_failure = self.grand_failure

        grand_skipped = self.grand_skipped

        errors: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        last_processed_record_number = self.last_processed_record_number

        total_rows = self.total_rows

        failed_rows = self.failed_rows

        failed_cells_count = self.failed_cells_count

        total_columns = self.total_columns

        existing_cells = self.existing_cells

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if grand_failure is not UNSET:
            field_dict["grandFailure"] = grand_failure
        if grand_skipped is not UNSET:
            field_dict["grandSkipped"] = grand_skipped
        if errors is not UNSET:
            field_dict["errors"] = errors
        if type is not UNSET:
            field_dict["type"] = type
        if last_processed_record_number is not UNSET:
            field_dict["lastProcessedRecordNumber"] = last_processed_record_number
        if total_rows is not UNSET:
            field_dict["totalRows"] = total_rows
        if failed_rows is not UNSET:
            field_dict["failedRows"] = failed_rows
        if failed_cells_count is not UNSET:
            field_dict["failedCellsCount"] = failed_cells_count
        if total_columns is not UNSET:
            field_dict["totalColumns"] = total_columns
        if existing_cells is not UNSET:
            field_dict["existingCells"] = existing_cells

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.xlsx_parsing_error_model import XlsxParsingErrorModel

        d = src_dict.copy()
        grand_failure = d.pop("grandFailure", UNSET)

        grand_skipped = d.pop("grandSkipped", UNSET)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = XlsxParsingErrorModel.from_dict(errors_item_data)

            errors.append(errors_item)

        _type = d.pop("type", UNSET)
        type: Union[Unset, AbstractImportFileProgressType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AbstractImportFileProgressType(_type)

        last_processed_record_number = d.pop("lastProcessedRecordNumber", UNSET)

        total_rows = d.pop("totalRows", UNSET)

        failed_rows = d.pop("failedRows", UNSET)

        failed_cells_count = d.pop("failedCellsCount", UNSET)

        total_columns = d.pop("totalColumns", UNSET)

        existing_cells = d.pop("existingCells", UNSET)

        abstract_import_file_progress = cls(
            grand_failure=grand_failure,
            grand_skipped=grand_skipped,
            errors=errors,
            type=type,
            last_processed_record_number=last_processed_record_number,
            total_rows=total_rows,
            failed_rows=failed_rows,
            failed_cells_count=failed_cells_count,
            total_columns=total_columns,
            existing_cells=existing_cells,
        )

        abstract_import_file_progress.additional_properties = d
        return abstract_import_file_progress

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
