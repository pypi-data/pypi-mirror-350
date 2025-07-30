from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="AuthenticationTokenDto")


@_attrs_define
class AuthenticationTokenDto:
    """
    Attributes:
        token (Union[Unset, str]):
        token_type (Union[Unset, str]):
        expires_in (Union[Unset, int]):
        refresh_token (Union[Unset, str]):
        expiration_time (Union[Unset, int]):
    """

    token: Union[Unset, str] = UNSET
    token_type: Union[Unset, str] = UNSET
    expires_in: Union[Unset, int] = UNSET
    refresh_token: Union[Unset, str] = UNSET
    expiration_time: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        token = self.token

        token_type = self.token_type

        expires_in = self.expires_in

        refresh_token = self.refresh_token

        expiration_time = self.expiration_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if token is not UNSET:
            field_dict["token"] = token
        if token_type is not UNSET:
            field_dict["tokenType"] = token_type
        if expires_in is not UNSET:
            field_dict["expiresIn"] = expires_in
        if refresh_token is not UNSET:
            field_dict["refreshToken"] = refresh_token
        if expiration_time is not UNSET:
            field_dict["expirationTime"] = expiration_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        token = d.pop("token", UNSET)

        token_type = d.pop("tokenType", UNSET)

        expires_in = d.pop("expiresIn", UNSET)

        refresh_token = d.pop("refreshToken", UNSET)

        expiration_time = d.pop("expirationTime", UNSET)

        authentication_token_dto = cls(
            token=token,
            token_type=token_type,
            expires_in=expires_in,
            refresh_token=refresh_token,
            expiration_time=expiration_time,
        )

        authentication_token_dto.additional_properties = d
        return authentication_token_dto

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
