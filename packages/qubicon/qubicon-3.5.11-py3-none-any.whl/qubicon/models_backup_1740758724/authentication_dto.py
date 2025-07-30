from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.authentication_token_dto import AuthenticationTokenDto


T = TypeVar("T", bound="AuthenticationDto")


@_attrs_define
class AuthenticationDto:
    """
    Attributes:
        normal (Union[Unset, AuthenticationTokenDto]):
        monitor (Union[Unset, AuthenticationTokenDto]):
    """

    normal: Union[Unset, "AuthenticationTokenDto"] = UNSET
    monitor: Union[Unset, "AuthenticationTokenDto"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        normal: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.normal, Unset):
            normal = self.normal.to_dict()

        monitor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.monitor, Unset):
            monitor = self.monitor.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if normal is not UNSET:
            field_dict["normal"] = normal
        if monitor is not UNSET:
            field_dict["monitor"] = monitor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.authentication_token_dto import AuthenticationTokenDto

        d = src_dict.copy()
        _normal = d.pop("normal", UNSET)
        normal: Union[Unset, AuthenticationTokenDto]
        if isinstance(_normal, Unset):
            normal = UNSET
        else:
            normal = AuthenticationTokenDto.from_dict(_normal)

        _monitor = d.pop("monitor", UNSET)
        monitor: Union[Unset, AuthenticationTokenDto]
        if isinstance(_monitor, Unset):
            monitor = UNSET
        else:
            monitor = AuthenticationTokenDto.from_dict(_monitor)

        authentication_dto = cls(
            normal=normal,
            monitor=monitor,
        )

        authentication_dto.additional_properties = d
        return authentication_dto

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
