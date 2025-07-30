from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_login_dto_login_type import UserLoginDtoLoginType

T = TypeVar("T", bound="UserLoginDto")


@_attrs_define
class UserLoginDto:
    """
    Attributes:
        username (str):
        password (str):
        login_type (UserLoginDtoLoginType):
    """

    username: str
    password: str
    login_type: UserLoginDtoLoginType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        password = self.password

        login_type = self.login_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
                "loginType": login_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        login_type = UserLoginDtoLoginType(d.pop("loginType"))

        user_login_dto = cls(
            username=username,
            password=password,
            login_type=login_type,
        )

        user_login_dto.additional_properties = d
        return user_login_dto

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
