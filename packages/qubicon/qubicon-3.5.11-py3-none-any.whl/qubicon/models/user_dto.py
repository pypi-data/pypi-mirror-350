from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_dto_login_type import UserDtoLoginType
from ..models.user_dto_user_deactivation_reason import UserDtoUserDeactivationReason
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.privilege_dto import PrivilegeDto
    from ..models.role_dto import RoleDto
    from ..models.stream_dto import StreamDto


T = TypeVar("T", bound="UserDto")


@_attrs_define
class UserDto:
    """
    Attributes:
        name (str):
        first_name (str):
        last_name (str):
        email (str):
        roles (List['RoleDto']):
        id (Union[Unset, int]):
        activated (Union[Unset, bool]):
        gmp_enabled (Union[Unset, bool]):
        email_confirmed (Union[Unset, bool]):
        phone_sms_alerts (Union[Unset, str]):
        streams (Union[Unset, List['StreamDto']]):
        privileges (Union[Unset, List['PrivilegeDto']]):
        creation_date (Union[Unset, int]):
        update_date (Union[Unset, int]):
        failed_login_attempts (Union[Unset, int]):
        deactivation_time (Union[Unset, int]):
        activation_time (Union[Unset, int]):
        password_change_date (Union[Unset, int]):
        login_type (Union[Unset, UserDtoLoginType]):
        ldap_cn (Union[Unset, str]):
        user_deactivation_reason (Union[Unset, UserDtoUserDeactivationReason]):
        oauth_password_is_set (Union[Unset, bool]):
        oauth_id (Union[Unset, str]):
    """

    name: str
    first_name: str
    last_name: str
    email: str
    roles: List["RoleDto"]
    id: Union[Unset, int] = UNSET
    activated: Union[Unset, bool] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    email_confirmed: Union[Unset, bool] = UNSET
    phone_sms_alerts: Union[Unset, str] = UNSET
    streams: Union[Unset, List["StreamDto"]] = UNSET
    privileges: Union[Unset, List["PrivilegeDto"]] = UNSET
    creation_date: Union[Unset, int] = UNSET
    update_date: Union[Unset, int] = UNSET
    failed_login_attempts: Union[Unset, int] = UNSET
    deactivation_time: Union[Unset, int] = UNSET
    activation_time: Union[Unset, int] = UNSET
    password_change_date: Union[Unset, int] = UNSET
    login_type: Union[Unset, UserDtoLoginType] = UNSET
    ldap_cn: Union[Unset, str] = UNSET
    user_deactivation_reason: Union[Unset, UserDtoUserDeactivationReason] = UNSET
    oauth_password_is_set: Union[Unset, bool] = UNSET
    oauth_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        first_name = self.first_name

        last_name = self.last_name

        email = self.email

        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()
            roles.append(roles_item)

        id = self.id

        activated = self.activated

        gmp_enabled = self.gmp_enabled

        email_confirmed = self.email_confirmed

        phone_sms_alerts = self.phone_sms_alerts

        streams: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.streams, Unset):
            streams = []
            for streams_item_data in self.streams:
                streams_item = streams_item_data.to_dict()
                streams.append(streams_item)

        privileges: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.privileges, Unset):
            privileges = []
            for privileges_item_data in self.privileges:
                privileges_item = privileges_item_data.to_dict()
                privileges.append(privileges_item)

        creation_date = self.creation_date

        update_date = self.update_date

        failed_login_attempts = self.failed_login_attempts

        deactivation_time = self.deactivation_time

        activation_time = self.activation_time

        password_change_date = self.password_change_date

        login_type: Union[Unset, str] = UNSET
        if not isinstance(self.login_type, Unset):
            login_type = self.login_type.value

        ldap_cn = self.ldap_cn

        user_deactivation_reason: Union[Unset, str] = UNSET
        if not isinstance(self.user_deactivation_reason, Unset):
            user_deactivation_reason = self.user_deactivation_reason.value

        oauth_password_is_set = self.oauth_password_is_set

        oauth_id = self.oauth_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "roles": roles,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if activated is not UNSET:
            field_dict["activated"] = activated
        if gmp_enabled is not UNSET:
            field_dict["gmpEnabled"] = gmp_enabled
        if email_confirmed is not UNSET:
            field_dict["emailConfirmed"] = email_confirmed
        if phone_sms_alerts is not UNSET:
            field_dict["phoneSmsAlerts"] = phone_sms_alerts
        if streams is not UNSET:
            field_dict["streams"] = streams
        if privileges is not UNSET:
            field_dict["privileges"] = privileges
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date
        if failed_login_attempts is not UNSET:
            field_dict["failedLoginAttempts"] = failed_login_attempts
        if deactivation_time is not UNSET:
            field_dict["deactivationTime"] = deactivation_time
        if activation_time is not UNSET:
            field_dict["activationTime"] = activation_time
        if password_change_date is not UNSET:
            field_dict["passwordChangeDate"] = password_change_date
        if login_type is not UNSET:
            field_dict["loginType"] = login_type
        if ldap_cn is not UNSET:
            field_dict["ldapCn"] = ldap_cn
        if user_deactivation_reason is not UNSET:
            field_dict["userDeactivationReason"] = user_deactivation_reason
        if oauth_password_is_set is not UNSET:
            field_dict["oauthPasswordIsSet"] = oauth_password_is_set
        if oauth_id is not UNSET:
            field_dict["oauthId"] = oauth_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.privilege_dto import PrivilegeDto
        from ..models.role_dto import RoleDto
        from ..models.stream_dto import StreamDto

        d = src_dict.copy()
        name = d.pop("name")

        first_name = d.pop("firstName")

        last_name = d.pop("lastName")

        email = d.pop("email")

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = RoleDto.from_dict(roles_item_data)

            roles.append(roles_item)

        id = d.pop("id", UNSET)

        activated = d.pop("activated", UNSET)

        gmp_enabled = d.pop("gmpEnabled", UNSET)

        email_confirmed = d.pop("emailConfirmed", UNSET)

        phone_sms_alerts = d.pop("phoneSmsAlerts", UNSET)

        streams = []
        _streams = d.pop("streams", UNSET)
        for streams_item_data in _streams or []:
            streams_item = StreamDto.from_dict(streams_item_data)

            streams.append(streams_item)

        privileges = []
        _privileges = d.pop("privileges", UNSET)
        for privileges_item_data in _privileges or []:
            privileges_item = PrivilegeDto.from_dict(privileges_item_data)

            privileges.append(privileges_item)

        creation_date = d.pop("creationDate", UNSET)

        update_date = d.pop("updateDate", UNSET)

        failed_login_attempts = d.pop("failedLoginAttempts", UNSET)

        deactivation_time = d.pop("deactivationTime", UNSET)

        activation_time = d.pop("activationTime", UNSET)

        password_change_date = d.pop("passwordChangeDate", UNSET)

        _login_type = d.pop("loginType", UNSET)
        login_type: Union[Unset, UserDtoLoginType]
        if isinstance(_login_type, Unset):
            login_type = UNSET
        else:
            login_type = UserDtoLoginType(_login_type)

        ldap_cn = d.pop("ldapCn", UNSET)

        _user_deactivation_reason = d.pop("userDeactivationReason", UNSET)
        user_deactivation_reason: Union[Unset, UserDtoUserDeactivationReason]
        if isinstance(_user_deactivation_reason, Unset):
            user_deactivation_reason = UNSET
        else:
            user_deactivation_reason = UserDtoUserDeactivationReason(_user_deactivation_reason)

        oauth_password_is_set = d.pop("oauthPasswordIsSet", UNSET)

        oauth_id = d.pop("oauthId", UNSET)

        user_dto = cls(
            name=name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            roles=roles,
            id=id,
            activated=activated,
            gmp_enabled=gmp_enabled,
            email_confirmed=email_confirmed,
            phone_sms_alerts=phone_sms_alerts,
            streams=streams,
            privileges=privileges,
            creation_date=creation_date,
            update_date=update_date,
            failed_login_attempts=failed_login_attempts,
            deactivation_time=deactivation_time,
            activation_time=activation_time,
            password_change_date=password_change_date,
            login_type=login_type,
            ldap_cn=ldap_cn,
            user_deactivation_reason=user_deactivation_reason,
            oauth_password_is_set=oauth_password_is_set,
            oauth_id=oauth_id,
        )

        user_dto.additional_properties = d
        return user_dto

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
