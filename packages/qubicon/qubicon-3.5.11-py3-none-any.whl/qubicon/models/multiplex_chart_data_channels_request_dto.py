from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.channel_data_channel_request_key_dto import ChannelDataChannelRequestKeyDto


T = TypeVar("T", bound="MultiplexChartDataChannelsRequestDto")


@_attrs_define
class MultiplexChartDataChannelsRequestDto:
    """
    Attributes:
        channels (List['ChannelDataChannelRequestKeyDto']):
    """

    channels: List["ChannelDataChannelRequestKeyDto"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels = []
        for channels_item_data in self.channels:
            channels_item = channels_item_data.to_dict()
            channels.append(channels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "channels": channels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.channel_data_channel_request_key_dto import ChannelDataChannelRequestKeyDto

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels")
        for channels_item_data in _channels:
            channels_item = ChannelDataChannelRequestKeyDto.from_dict(channels_item_data)

            channels.append(channels_item)

        multiplex_chart_data_channels_request_dto = cls(
            channels=channels,
        )

        multiplex_chart_data_channels_request_dto.additional_properties = d
        return multiplex_chart_data_channels_request_dto

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
