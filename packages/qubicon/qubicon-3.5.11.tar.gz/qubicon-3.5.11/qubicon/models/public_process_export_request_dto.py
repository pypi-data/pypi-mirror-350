from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="PublicProcessExportRequestDto")


@_attrs_define
class PublicProcessExportRequestDto:
    """
    Attributes:
        raw_mode (Union[Unset, bool]):
        export_rate (Union[Unset, int]):
        at_sampling_timestamps_mode (Union[Unset, bool]):
        included_report (Union[Unset, bool]):
        start_event_id (Union[Unset, int]):
        end_event_id (Union[Unset, int]):
        start_time (Union[Unset, int]):
        end_time (Union[Unset, int]):
    """

    raw_mode: Union[Unset, bool] = UNSET
    export_rate: Union[Unset, int] = UNSET
    at_sampling_timestamps_mode: Union[Unset, bool] = UNSET
    included_report: Union[Unset, bool] = UNSET
    start_event_id: Union[Unset, int] = UNSET
    end_event_id: Union[Unset, int] = UNSET
    start_time: Union[Unset, int] = UNSET
    end_time: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        raw_mode = self.raw_mode

        export_rate = self.export_rate

        at_sampling_timestamps_mode = self.at_sampling_timestamps_mode

        included_report = self.included_report

        start_event_id = self.start_event_id

        end_event_id = self.end_event_id

        start_time = self.start_time

        end_time = self.end_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if raw_mode is not UNSET:
            field_dict["rawMode"] = raw_mode
        if export_rate is not UNSET:
            field_dict["exportRate"] = export_rate
        if at_sampling_timestamps_mode is not UNSET:
            field_dict["atSamplingTimestampsMode"] = at_sampling_timestamps_mode
        if included_report is not UNSET:
            field_dict["includedReport"] = included_report
        if start_event_id is not UNSET:
            field_dict["startEventId"] = start_event_id
        if end_event_id is not UNSET:
            field_dict["endEventId"] = end_event_id
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        raw_mode = d.pop("rawMode", UNSET)

        export_rate = d.pop("exportRate", UNSET)

        at_sampling_timestamps_mode = d.pop("atSamplingTimestampsMode", UNSET)

        included_report = d.pop("includedReport", UNSET)

        start_event_id = d.pop("startEventId", UNSET)

        end_event_id = d.pop("endEventId", UNSET)

        start_time = d.pop("startTime", UNSET)

        end_time = d.pop("endTime", UNSET)

        public_process_export_request_dto = cls(
            raw_mode=raw_mode,
            export_rate=export_rate,
            at_sampling_timestamps_mode=at_sampling_timestamps_mode,
            included_report=included_report,
            start_event_id=start_event_id,
            end_event_id=end_event_id,
            start_time=start_time,
            end_time=end_time,
        )

        public_process_export_request_dto.additional_properties = d
        return public_process_export_request_dto

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
