from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.channel_data_dto import ChannelDataDto
    from ..models.channel_data_key_dto import ChannelDataKeyDto


T = TypeVar("T", bound="ChannelDataPairDto")


@_attrs_define
class ChannelDataPairDto:
    """
    Attributes:
        key (Union[Unset, ChannelDataKeyDto]):
        value (Union[Unset, List['ChannelDataDto']]):
    """

    key: Union[Unset, "ChannelDataKeyDto"] = UNSET
    value: Union[Unset, List["ChannelDataDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.key, Unset):
            key = self.key.to_dict()

        value: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.value, Unset):
            value = []
            for value_item_data in self.value:
                value_item = value_item_data.to_dict()
                value.append(value_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.channel_data_dto import ChannelDataDto
        from ..models.channel_data_key_dto import ChannelDataKeyDto

        d = src_dict.copy()
        _key = d.pop("key", UNSET)
        key: Union[Unset, ChannelDataKeyDto]
        if isinstance(_key, Unset):
            key = UNSET
        else:
            key = ChannelDataKeyDto.from_dict(_key)

        value = []
        _value = d.pop("value", UNSET)
        for value_item_data in _value or []:
            value_item = ChannelDataDto.from_dict(value_item_data)

            value.append(value_item)

        channel_data_pair_dto = cls(
            key=key,
            value=value,
        )

        channel_data_pair_dto.additional_properties = d
        return channel_data_pair_dto

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
