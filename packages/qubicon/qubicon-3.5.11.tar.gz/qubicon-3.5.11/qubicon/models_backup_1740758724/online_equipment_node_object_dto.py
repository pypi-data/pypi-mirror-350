from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.online_equipment_node_object_dto_equipment_type import OnlineEquipmentNodeObjectDtoEquipmentType
from ..models.online_equipment_node_object_dto_node_opc_ua_type import OnlineEquipmentNodeObjectDtoNodeOpcUaType
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="OnlineEquipmentNodeObjectDto")


@_attrs_define
class OnlineEquipmentNodeObjectDto:
    """
    Attributes:
        id (int):
        opc_ua_server_id (Union[Unset, int]):
        equipment_id (Union[Unset, int]):
        gmp_enabled (Union[Unset, bool]):
        opc_ua_server_name (Union[Unset, str]):
        equipment_name (Union[Unset, str]):
        browse_name (Union[Unset, str]):
        display_name (Union[Unset, str]):
        description (Union[Unset, str]):
        node_opc_ua_id (Union[Unset, str]):
        tag_name (Union[Unset, str]):
        qubicon_name (Union[Unset, str]):
        equipment_type (Union[Unset, OnlineEquipmentNodeObjectDtoEquipmentType]):
        node_opc_ua_type (Union[Unset, OnlineEquipmentNodeObjectDtoNodeOpcUaType]):
        mapped (Union[Unset, bool]):
        monitored (Union[Unset, bool]):
        health_status (Union[Unset, bool]):
        health_last_check_time (Union[Unset, int]):
        favorite (Union[Unset, bool]):
    """

    id: int
    opc_ua_server_id: Union[Unset, int] = UNSET
    equipment_id: Union[Unset, int] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    opc_ua_server_name: Union[Unset, str] = UNSET
    equipment_name: Union[Unset, str] = UNSET
    browse_name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    node_opc_ua_id: Union[Unset, str] = UNSET
    tag_name: Union[Unset, str] = UNSET
    qubicon_name: Union[Unset, str] = UNSET
    equipment_type: Union[Unset, OnlineEquipmentNodeObjectDtoEquipmentType] = UNSET
    node_opc_ua_type: Union[Unset, OnlineEquipmentNodeObjectDtoNodeOpcUaType] = UNSET
    mapped: Union[Unset, bool] = UNSET
    monitored: Union[Unset, bool] = UNSET
    health_status: Union[Unset, bool] = UNSET
    health_last_check_time: Union[Unset, int] = UNSET
    favorite: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        opc_ua_server_id = self.opc_ua_server_id

        equipment_id = self.equipment_id

        gmp_enabled = self.gmp_enabled

        opc_ua_server_name = self.opc_ua_server_name

        equipment_name = self.equipment_name

        browse_name = self.browse_name

        display_name = self.display_name

        description = self.description

        node_opc_ua_id = self.node_opc_ua_id

        tag_name = self.tag_name

        qubicon_name = self.qubicon_name

        equipment_type: Union[Unset, str] = UNSET
        if not isinstance(self.equipment_type, Unset):
            equipment_type = self.equipment_type.value

        node_opc_ua_type: Union[Unset, str] = UNSET
        if not isinstance(self.node_opc_ua_type, Unset):
            node_opc_ua_type = self.node_opc_ua_type.value

        mapped = self.mapped

        monitored = self.monitored

        health_status = self.health_status

        health_last_check_time = self.health_last_check_time

        favorite = self.favorite

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if opc_ua_server_id is not UNSET:
            field_dict["opcUaServerId"] = opc_ua_server_id
        if equipment_id is not UNSET:
            field_dict["equipmentId"] = equipment_id
        if gmp_enabled is not UNSET:
            field_dict["gmpEnabled"] = gmp_enabled
        if opc_ua_server_name is not UNSET:
            field_dict["opcUaServerName"] = opc_ua_server_name
        if equipment_name is not UNSET:
            field_dict["equipmentName"] = equipment_name
        if browse_name is not UNSET:
            field_dict["browseName"] = browse_name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if description is not UNSET:
            field_dict["description"] = description
        if node_opc_ua_id is not UNSET:
            field_dict["nodeOpcUaId"] = node_opc_ua_id
        if tag_name is not UNSET:
            field_dict["tagName"] = tag_name
        if qubicon_name is not UNSET:
            field_dict["qubiconName"] = qubicon_name
        if equipment_type is not UNSET:
            field_dict["equipmentType"] = equipment_type
        if node_opc_ua_type is not UNSET:
            field_dict["nodeOpcUaType"] = node_opc_ua_type
        if mapped is not UNSET:
            field_dict["mapped"] = mapped
        if monitored is not UNSET:
            field_dict["monitored"] = monitored
        if health_status is not UNSET:
            field_dict["healthStatus"] = health_status
        if health_last_check_time is not UNSET:
            field_dict["healthLastCheckTime"] = health_last_check_time
        if favorite is not UNSET:
            field_dict["favorite"] = favorite

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        opc_ua_server_id = d.pop("opcUaServerId", UNSET)

        equipment_id = d.pop("equipmentId", UNSET)

        gmp_enabled = d.pop("gmpEnabled", UNSET)

        opc_ua_server_name = d.pop("opcUaServerName", UNSET)

        equipment_name = d.pop("equipmentName", UNSET)

        browse_name = d.pop("browseName", UNSET)

        display_name = d.pop("displayName", UNSET)

        description = d.pop("description", UNSET)

        node_opc_ua_id = d.pop("nodeOpcUaId", UNSET)

        tag_name = d.pop("tagName", UNSET)

        qubicon_name = d.pop("qubiconName", UNSET)

        _equipment_type = d.pop("equipmentType", UNSET)
        equipment_type: Union[Unset, OnlineEquipmentNodeObjectDtoEquipmentType]
        if isinstance(_equipment_type, Unset):
            equipment_type = UNSET
        else:
            equipment_type = OnlineEquipmentNodeObjectDtoEquipmentType(_equipment_type)

        _node_opc_ua_type = d.pop("nodeOpcUaType", UNSET)
        node_opc_ua_type: Union[Unset, OnlineEquipmentNodeObjectDtoNodeOpcUaType]
        if isinstance(_node_opc_ua_type, Unset):
            node_opc_ua_type = UNSET
        else:
            node_opc_ua_type = OnlineEquipmentNodeObjectDtoNodeOpcUaType(_node_opc_ua_type)

        mapped = d.pop("mapped", UNSET)

        monitored = d.pop("monitored", UNSET)

        health_status = d.pop("healthStatus", UNSET)

        health_last_check_time = d.pop("healthLastCheckTime", UNSET)

        favorite = d.pop("favorite", UNSET)

        online_equipment_node_object_dto = cls(
            id=id,
            opc_ua_server_id=opc_ua_server_id,
            equipment_id=equipment_id,
            gmp_enabled=gmp_enabled,
            opc_ua_server_name=opc_ua_server_name,
            equipment_name=equipment_name,
            browse_name=browse_name,
            display_name=display_name,
            description=description,
            node_opc_ua_id=node_opc_ua_id,
            tag_name=tag_name,
            qubicon_name=qubicon_name,
            equipment_type=equipment_type,
            node_opc_ua_type=node_opc_ua_type,
            mapped=mapped,
            monitored=monitored,
            health_status=health_status,
            health_last_check_time=health_last_check_time,
            favorite=favorite,
        )

        online_equipment_node_object_dto.additional_properties = d
        return online_equipment_node_object_dto

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
