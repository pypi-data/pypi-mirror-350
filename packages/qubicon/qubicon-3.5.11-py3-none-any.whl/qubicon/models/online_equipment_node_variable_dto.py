from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.online_equipment_node_variable_dto_equipment_type import OnlineEquipmentNodeVariableDtoEquipmentType
from ..models.online_equipment_node_variable_dto_node_opc_ua_type import OnlineEquipmentNodeVariableDtoNodeOpcUaType
from ..models.online_equipment_node_variable_dto_signal_type import OnlineEquipmentNodeVariableDtoSignalType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto
    from ..models.publish_schema_dto import PublishSchemaDto
    from ..models.sensor_type_dto import SensorTypeDto


T = TypeVar("T", bound="OnlineEquipmentNodeVariableDto")


@_attrs_define
class OnlineEquipmentNodeVariableDto:
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
        equipment_type (Union[Unset, OnlineEquipmentNodeVariableDtoEquipmentType]):
        node_opc_ua_type (Union[Unset, OnlineEquipmentNodeVariableDtoNodeOpcUaType]):
        mapped (Union[Unset, bool]):
        monitored (Union[Unset, bool]):
        health_status (Union[Unset, bool]):
        health_last_check_time (Union[Unset, int]):
        favorite (Union[Unset, bool]):
        opc_ua_data_type (Union[Unset, str]):
        compatible_data_type (Union[Unset, str]):
        physical_quantity_unit (Union[Unset, PhysicalQuantityUnitDto]):
        sensor_type (Union[Unset, SensorTypeDto]):
        signal_type (Union[Unset, OnlineEquipmentNodeVariableDtoSignalType]):
        actual_state_value (Union[Unset, str]):
        actual_state_change_time (Union[Unset, int]):
        min_value (Union[Unset, float]):
        max_value (Union[Unset, float]):
        publish_schema (Union[Unset, PublishSchemaDto]):
        single_value (Union[Unset, bool]):
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
    equipment_type: Union[Unset, OnlineEquipmentNodeVariableDtoEquipmentType] = UNSET
    node_opc_ua_type: Union[Unset, OnlineEquipmentNodeVariableDtoNodeOpcUaType] = UNSET
    mapped: Union[Unset, bool] = UNSET
    monitored: Union[Unset, bool] = UNSET
    health_status: Union[Unset, bool] = UNSET
    health_last_check_time: Union[Unset, int] = UNSET
    favorite: Union[Unset, bool] = UNSET
    opc_ua_data_type: Union[Unset, str] = UNSET
    compatible_data_type: Union[Unset, str] = UNSET
    physical_quantity_unit: Union[Unset, "PhysicalQuantityUnitDto"] = UNSET
    sensor_type: Union[Unset, "SensorTypeDto"] = UNSET
    signal_type: Union[Unset, OnlineEquipmentNodeVariableDtoSignalType] = UNSET
    actual_state_value: Union[Unset, str] = UNSET
    actual_state_change_time: Union[Unset, int] = UNSET
    min_value: Union[Unset, float] = UNSET
    max_value: Union[Unset, float] = UNSET
    publish_schema: Union[Unset, "PublishSchemaDto"] = UNSET
    single_value: Union[Unset, bool] = UNSET
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

        opc_ua_data_type = self.opc_ua_data_type

        compatible_data_type = self.compatible_data_type

        physical_quantity_unit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.physical_quantity_unit, Unset):
            physical_quantity_unit = self.physical_quantity_unit.to_dict()

        sensor_type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sensor_type, Unset):
            sensor_type = self.sensor_type.to_dict()

        signal_type: Union[Unset, str] = UNSET
        if not isinstance(self.signal_type, Unset):
            signal_type = self.signal_type.value

        actual_state_value = self.actual_state_value

        actual_state_change_time = self.actual_state_change_time

        min_value = self.min_value

        max_value = self.max_value

        publish_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.publish_schema, Unset):
            publish_schema = self.publish_schema.to_dict()

        single_value = self.single_value

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
        if opc_ua_data_type is not UNSET:
            field_dict["opcUaDataType"] = opc_ua_data_type
        if compatible_data_type is not UNSET:
            field_dict["compatibleDataType"] = compatible_data_type
        if physical_quantity_unit is not UNSET:
            field_dict["physicalQuantityUnit"] = physical_quantity_unit
        if sensor_type is not UNSET:
            field_dict["sensorType"] = sensor_type
        if signal_type is not UNSET:
            field_dict["signalType"] = signal_type
        if actual_state_value is not UNSET:
            field_dict["actualStateValue"] = actual_state_value
        if actual_state_change_time is not UNSET:
            field_dict["actualStateChangeTime"] = actual_state_change_time
        if min_value is not UNSET:
            field_dict["minValue"] = min_value
        if max_value is not UNSET:
            field_dict["maxValue"] = max_value
        if publish_schema is not UNSET:
            field_dict["publishSchema"] = publish_schema
        if single_value is not UNSET:
            field_dict["singleValue"] = single_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto
        from ..models.publish_schema_dto import PublishSchemaDto
        from ..models.sensor_type_dto import SensorTypeDto

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
        equipment_type: Union[Unset, OnlineEquipmentNodeVariableDtoEquipmentType]
        if isinstance(_equipment_type, Unset):
            equipment_type = UNSET
        else:
            equipment_type = OnlineEquipmentNodeVariableDtoEquipmentType(_equipment_type)

        _node_opc_ua_type = d.pop("nodeOpcUaType", UNSET)
        node_opc_ua_type: Union[Unset, OnlineEquipmentNodeVariableDtoNodeOpcUaType]
        if isinstance(_node_opc_ua_type, Unset):
            node_opc_ua_type = UNSET
        else:
            node_opc_ua_type = OnlineEquipmentNodeVariableDtoNodeOpcUaType(_node_opc_ua_type)

        mapped = d.pop("mapped", UNSET)

        monitored = d.pop("monitored", UNSET)

        health_status = d.pop("healthStatus", UNSET)

        health_last_check_time = d.pop("healthLastCheckTime", UNSET)

        favorite = d.pop("favorite", UNSET)

        opc_ua_data_type = d.pop("opcUaDataType", UNSET)

        compatible_data_type = d.pop("compatibleDataType", UNSET)

        _physical_quantity_unit = d.pop("physicalQuantityUnit", UNSET)
        physical_quantity_unit: Union[Unset, PhysicalQuantityUnitDto]
        if isinstance(_physical_quantity_unit, Unset):
            physical_quantity_unit = UNSET
        else:
            physical_quantity_unit = PhysicalQuantityUnitDto.from_dict(_physical_quantity_unit)

        _sensor_type = d.pop("sensorType", UNSET)
        sensor_type: Union[Unset, SensorTypeDto]
        if isinstance(_sensor_type, Unset):
            sensor_type = UNSET
        else:
            sensor_type = SensorTypeDto.from_dict(_sensor_type)

        _signal_type = d.pop("signalType", UNSET)
        signal_type: Union[Unset, OnlineEquipmentNodeVariableDtoSignalType]
        if isinstance(_signal_type, Unset):
            signal_type = UNSET
        else:
            signal_type = OnlineEquipmentNodeVariableDtoSignalType(_signal_type)

        actual_state_value = d.pop("actualStateValue", UNSET)

        actual_state_change_time = d.pop("actualStateChangeTime", UNSET)

        min_value = d.pop("minValue", UNSET)

        max_value = d.pop("maxValue", UNSET)

        _publish_schema = d.pop("publishSchema", UNSET)
        publish_schema: Union[Unset, PublishSchemaDto]
        if isinstance(_publish_schema, Unset):
            publish_schema = UNSET
        else:
            publish_schema = PublishSchemaDto.from_dict(_publish_schema)

        single_value = d.pop("singleValue", UNSET)

        online_equipment_node_variable_dto = cls(
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
            opc_ua_data_type=opc_ua_data_type,
            compatible_data_type=compatible_data_type,
            physical_quantity_unit=physical_quantity_unit,
            sensor_type=sensor_type,
            signal_type=signal_type,
            actual_state_value=actual_state_value,
            actual_state_change_time=actual_state_change_time,
            min_value=min_value,
            max_value=max_value,
            publish_schema=publish_schema,
            single_value=single_value,
        )

        online_equipment_node_variable_dto.additional_properties = d
        return online_equipment_node_variable_dto

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
