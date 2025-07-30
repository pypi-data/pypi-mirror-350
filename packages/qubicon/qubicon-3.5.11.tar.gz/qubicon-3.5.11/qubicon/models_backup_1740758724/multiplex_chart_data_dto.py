from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.channel_data_pair_dto import ChannelDataPairDto


T = TypeVar("T", bound="MultiplexChartDataDto")


@_attrs_define
class MultiplexChartDataDto:
    """
    Attributes:
        channels (Union[Unset, List['ChannelDataPairDto']]):
    """

    channels: Union[Unset, List["ChannelDataPairDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        channels: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.channels, Unset):
            channels = []
            for channels_item_data in self.channels:
                channels_item = channels_item_data.to_dict()
                channels.append(channels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if channels is not UNSET:
            field_dict["channels"] = channels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.channel_data_pair_dto import ChannelDataPairDto

        d = src_dict.copy()
        channels = []
        _channels = d.pop("channels", UNSET)
        for channels_item_data in _channels or []:
            channels_item = ChannelDataPairDto.from_dict(channels_item_data)

            channels.append(channels_item)

        multiplex_chart_data_dto = cls(
            channels=channels,
        )

        multiplex_chart_data_dto.additional_properties = d
        return multiplex_chart_data_dto

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
