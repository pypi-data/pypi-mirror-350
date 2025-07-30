from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gmp_track_confirmation_dto_role import GmpTrackConfirmationDtoRole
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_dto import UserDto


T = TypeVar("T", bound="GmpTrackConfirmationDto")


@_attrs_define
class GmpTrackConfirmationDto:
    """
    Attributes:
        user (Union[Unset, UserDto]):
        when (Union[Unset, int]):
        approval (Union[Unset, bool]):
        confirmed_date (Union[Unset, int]):
        comment (Union[Unset, str]):
        role (Union[Unset, GmpTrackConfirmationDtoRole]):
    """

    user: Union[Unset, "UserDto"] = UNSET
    when: Union[Unset, int] = UNSET
    approval: Union[Unset, bool] = UNSET
    confirmed_date: Union[Unset, int] = UNSET
    comment: Union[Unset, str] = UNSET
    role: Union[Unset, GmpTrackConfirmationDtoRole] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        when = self.when

        approval = self.approval

        confirmed_date = self.confirmed_date

        comment = self.comment

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if when is not UNSET:
            field_dict["when"] = when
        if approval is not UNSET:
            field_dict["approval"] = approval
        if confirmed_date is not UNSET:
            field_dict["confirmedDate"] = confirmed_date
        if comment is not UNSET:
            field_dict["comment"] = comment
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_dto import UserDto

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, UserDto]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserDto.from_dict(_user)

        when = d.pop("when", UNSET)

        approval = d.pop("approval", UNSET)

        confirmed_date = d.pop("confirmedDate", UNSET)

        comment = d.pop("comment", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, GmpTrackConfirmationDtoRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = GmpTrackConfirmationDtoRole(_role)

        gmp_track_confirmation_dto = cls(
            user=user,
            when=when,
            approval=approval,
            confirmed_date=confirmed_date,
            comment=comment,
            role=role,
        )

        gmp_track_confirmation_dto.additional_properties = d
        return gmp_track_confirmation_dto

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
