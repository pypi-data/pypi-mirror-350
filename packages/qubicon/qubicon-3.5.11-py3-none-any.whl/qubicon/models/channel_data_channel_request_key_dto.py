from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_data_channel_request_key_dto_type import ChannelDataChannelRequestKeyDtoType
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="ChannelDataChannelRequestKeyDto")


@_attrs_define
class ChannelDataChannelRequestKeyDto:
    """
    Attributes:
        id (Union[Unset, int]):
        type (Union[Unset, ChannelDataChannelRequestKeyDtoType]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        forced_correction_by_client_utc_0_time (Union[Unset, int]):
        granularity (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    type: Union[Unset, ChannelDataChannelRequestKeyDtoType] = UNSET
    start_date: Union[Unset, int] = UNSET
    end_date: Union[Unset, int] = UNSET
    forced_correction_by_client_utc_0_time: Union[Unset, int] = UNSET
    granularity: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        start_date = self.start_date

        end_date = self.end_date

        forced_correction_by_client_utc_0_time = self.forced_correction_by_client_utc_0_time

        granularity = self.granularity

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if forced_correction_by_client_utc_0_time is not UNSET:
            field_dict["forcedCorrectionByClientUtc0Time"] = forced_correction_by_client_utc_0_time
        if granularity is not UNSET:
            field_dict["granularity"] = granularity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ChannelDataChannelRequestKeyDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ChannelDataChannelRequestKeyDtoType(_type)

        start_date = d.pop("startDate", UNSET)

        end_date = d.pop("endDate", UNSET)

        forced_correction_by_client_utc_0_time = d.pop("forcedCorrectionByClientUtc0Time", UNSET)

        granularity = d.pop("granularity", UNSET)

        channel_data_channel_request_key_dto = cls(
            id=id,
            type=type,
            start_date=start_date,
            end_date=end_date,
            forced_correction_by_client_utc_0_time=forced_correction_by_client_utc_0_time,
            granularity=granularity,
        )

        channel_data_channel_request_key_dto.additional_properties = d
        return channel_data_channel_request_key_dto

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
