from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.process_dto_process_archive_transition_status import ProcessDtoProcessArchiveTransitionStatus
from ..models.process_dto_python_engine_status import ProcessDtoPythonEngineStatus
from ..models.process_dto_status import ProcessDtoStatus
from ..models.process_dto_type import ProcessDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offline_equipment_dto import OfflineEquipmentDto
    from ..models.online_equipment_dto import OnlineEquipmentDto
    from ..models.process_phase_dto import ProcessPhaseDto


T = TypeVar("T", bound="ProcessDto")


@_attrs_define
class ProcessDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        description (Union[Unset, str]):
        update_date (Union[Unset, int]):
        creation_date (Union[Unset, int]):
        gmp_enabled (Union[Unset, bool]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        status (Union[Unset, ProcessDtoStatus]):
        publish_enabled (Union[Unset, bool]):
        publish_planned_at (Union[Unset, int]):
        imported (Union[Unset, bool]):
        import_date (Union[Unset, int]):
        last_usage_date (Union[Unset, int]):
        simulated (Union[Unset, bool]):
        python_engine_status (Union[Unset, ProcessDtoPythonEngineStatus]):
        type (Union[Unset, ProcessDtoType]):
        control_recipe_id (Union[Unset, int]):
        control_recipe_name (Union[Unset, str]):
        warm_up_date (Union[Unset, int]):
        python_online_calculator_restart_date (Union[Unset, int]):
        python_sampling_calculator_restart_date (Union[Unset, int]):
        media (Union[Unset, str]):
        buffer (Union[Unset, str]):
        process_archive_transition_status (Union[Unset, ProcessDtoProcessArchiveTransitionStatus]):
        current_phase (Union[Unset, ProcessPhaseDto]):
        online_equipment (Union[Unset, List['OnlineEquipmentDto']]):
        offline_equipment (Union[Unset, List['OfflineEquipmentDto']]):
        kpi_count (Union[Unset, int]):
        sensor_count (Union[Unset, int]):
        offline_sensor_count (Union[Unset, int]):
        online_sensor_count (Union[Unset, int]):
        has_draft_samplings (Union[Unset, bool]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    update_date: Union[Unset, int] = UNSET
    creation_date: Union[Unset, int] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    start_date: Union[Unset, int] = UNSET
    end_date: Union[Unset, int] = UNSET
    status: Union[Unset, ProcessDtoStatus] = UNSET
    publish_enabled: Union[Unset, bool] = UNSET
    publish_planned_at: Union[Unset, int] = UNSET
    imported: Union[Unset, bool] = UNSET
    import_date: Union[Unset, int] = UNSET
    last_usage_date: Union[Unset, int] = UNSET
    simulated: Union[Unset, bool] = UNSET
    python_engine_status: Union[Unset, ProcessDtoPythonEngineStatus] = UNSET
    type: Union[Unset, ProcessDtoType] = UNSET
    control_recipe_id: Union[Unset, int] = UNSET
    control_recipe_name: Union[Unset, str] = UNSET
    warm_up_date: Union[Unset, int] = UNSET
    python_online_calculator_restart_date: Union[Unset, int] = UNSET
    python_sampling_calculator_restart_date: Union[Unset, int] = UNSET
    media: Union[Unset, str] = UNSET
    buffer: Union[Unset, str] = UNSET
    process_archive_transition_status: Union[Unset, ProcessDtoProcessArchiveTransitionStatus] = UNSET
    current_phase: Union[Unset, "ProcessPhaseDto"] = UNSET
    online_equipment: Union[Unset, List["OnlineEquipmentDto"]] = UNSET
    offline_equipment: Union[Unset, List["OfflineEquipmentDto"]] = UNSET
    kpi_count: Union[Unset, int] = UNSET
    sensor_count: Union[Unset, int] = UNSET
    offline_sensor_count: Union[Unset, int] = UNSET
    online_sensor_count: Union[Unset, int] = UNSET
    has_draft_samplings: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        description = self.description

        update_date = self.update_date

        creation_date = self.creation_date

        gmp_enabled = self.gmp_enabled

        start_date = self.start_date

        end_date = self.end_date

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        publish_enabled = self.publish_enabled

        publish_planned_at = self.publish_planned_at

        imported = self.imported

        import_date = self.import_date

        last_usage_date = self.last_usage_date

        simulated = self.simulated

        python_engine_status: Union[Unset, str] = UNSET
        if not isinstance(self.python_engine_status, Unset):
            python_engine_status = self.python_engine_status.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        control_recipe_id = self.control_recipe_id

        control_recipe_name = self.control_recipe_name

        warm_up_date = self.warm_up_date

        python_online_calculator_restart_date = self.python_online_calculator_restart_date

        python_sampling_calculator_restart_date = self.python_sampling_calculator_restart_date

        media = self.media

        buffer = self.buffer

        process_archive_transition_status: Union[Unset, str] = UNSET
        if not isinstance(self.process_archive_transition_status, Unset):
            process_archive_transition_status = self.process_archive_transition_status.value

        current_phase: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.current_phase, Unset):
            current_phase = self.current_phase.to_dict()

        online_equipment: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.online_equipment, Unset):
            online_equipment = []
            for online_equipment_item_data in self.online_equipment:
                online_equipment_item = online_equipment_item_data.to_dict()
                online_equipment.append(online_equipment_item)

        offline_equipment: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.offline_equipment, Unset):
            offline_equipment = []
            for offline_equipment_item_data in self.offline_equipment:
                offline_equipment_item = offline_equipment_item_data.to_dict()
                offline_equipment.append(offline_equipment_item)

        kpi_count = self.kpi_count

        sensor_count = self.sensor_count

        offline_sensor_count = self.offline_sensor_count

        online_sensor_count = self.online_sensor_count

        has_draft_samplings = self.has_draft_samplings

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if description is not UNSET:
            field_dict["description"] = description
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if gmp_enabled is not UNSET:
            field_dict["gmpEnabled"] = gmp_enabled
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if status is not UNSET:
            field_dict["status"] = status
        if publish_enabled is not UNSET:
            field_dict["publishEnabled"] = publish_enabled
        if publish_planned_at is not UNSET:
            field_dict["publishPlannedAt"] = publish_planned_at
        if imported is not UNSET:
            field_dict["imported"] = imported
        if import_date is not UNSET:
            field_dict["importDate"] = import_date
        if last_usage_date is not UNSET:
            field_dict["lastUsageDate"] = last_usage_date
        if simulated is not UNSET:
            field_dict["simulated"] = simulated
        if python_engine_status is not UNSET:
            field_dict["pythonEngineStatus"] = python_engine_status
        if type is not UNSET:
            field_dict["type"] = type
        if control_recipe_id is not UNSET:
            field_dict["controlRecipeId"] = control_recipe_id
        if control_recipe_name is not UNSET:
            field_dict["controlRecipeName"] = control_recipe_name
        if warm_up_date is not UNSET:
            field_dict["warmUpDate"] = warm_up_date
        if python_online_calculator_restart_date is not UNSET:
            field_dict["pythonOnlineCalculatorRestartDate"] = python_online_calculator_restart_date
        if python_sampling_calculator_restart_date is not UNSET:
            field_dict["pythonSamplingCalculatorRestartDate"] = python_sampling_calculator_restart_date
        if media is not UNSET:
            field_dict["media"] = media
        if buffer is not UNSET:
            field_dict["buffer"] = buffer
        if process_archive_transition_status is not UNSET:
            field_dict["processArchiveTransitionStatus"] = process_archive_transition_status
        if current_phase is not UNSET:
            field_dict["currentPhase"] = current_phase
        if online_equipment is not UNSET:
            field_dict["onlineEquipment"] = online_equipment
        if offline_equipment is not UNSET:
            field_dict["offlineEquipment"] = offline_equipment
        if kpi_count is not UNSET:
            field_dict["kpiCount"] = kpi_count
        if sensor_count is not UNSET:
            field_dict["sensorCount"] = sensor_count
        if offline_sensor_count is not UNSET:
            field_dict["offlineSensorCount"] = offline_sensor_count
        if online_sensor_count is not UNSET:
            field_dict["onlineSensorCount"] = online_sensor_count
        if has_draft_samplings is not UNSET:
            field_dict["hasDraftSamplings"] = has_draft_samplings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.offline_equipment_dto import OfflineEquipmentDto
        from ..models.online_equipment_dto import OnlineEquipmentDto
        from ..models.process_phase_dto import ProcessPhaseDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        update_date = d.pop("updateDate", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        gmp_enabled = d.pop("gmpEnabled", UNSET)

        start_date = d.pop("startDate", UNSET)

        end_date = d.pop("endDate", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ProcessDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ProcessDtoStatus(_status)

        publish_enabled = d.pop("publishEnabled", UNSET)

        publish_planned_at = d.pop("publishPlannedAt", UNSET)

        imported = d.pop("imported", UNSET)

        import_date = d.pop("importDate", UNSET)

        last_usage_date = d.pop("lastUsageDate", UNSET)

        simulated = d.pop("simulated", UNSET)

        _python_engine_status = d.pop("pythonEngineStatus", UNSET)
        python_engine_status: Union[Unset, ProcessDtoPythonEngineStatus]
        if isinstance(_python_engine_status, Unset):
            python_engine_status = UNSET
        else:
            python_engine_status = ProcessDtoPythonEngineStatus(_python_engine_status)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ProcessDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ProcessDtoType(_type)

        control_recipe_id = d.pop("controlRecipeId", UNSET)

        control_recipe_name = d.pop("controlRecipeName", UNSET)

        warm_up_date = d.pop("warmUpDate", UNSET)

        python_online_calculator_restart_date = d.pop("pythonOnlineCalculatorRestartDate", UNSET)

        python_sampling_calculator_restart_date = d.pop("pythonSamplingCalculatorRestartDate", UNSET)

        media = d.pop("media", UNSET)

        buffer = d.pop("buffer", UNSET)

        _process_archive_transition_status = d.pop("processArchiveTransitionStatus", UNSET)
        process_archive_transition_status: Union[Unset, ProcessDtoProcessArchiveTransitionStatus]
        if isinstance(_process_archive_transition_status, Unset):
            process_archive_transition_status = UNSET
        else:
            process_archive_transition_status = ProcessDtoProcessArchiveTransitionStatus(
                _process_archive_transition_status
            )

        _current_phase = d.pop("currentPhase", UNSET)
        current_phase: Union[Unset, ProcessPhaseDto]
        if isinstance(_current_phase, Unset):
            current_phase = UNSET
        else:
            current_phase = ProcessPhaseDto.from_dict(_current_phase)

        online_equipment = []
        _online_equipment = d.pop("onlineEquipment", UNSET)
        for online_equipment_item_data in _online_equipment or []:
            online_equipment_item = OnlineEquipmentDto.from_dict(online_equipment_item_data)

            online_equipment.append(online_equipment_item)

        offline_equipment = []
        _offline_equipment = d.pop("offlineEquipment", UNSET)
        for offline_equipment_item_data in _offline_equipment or []:
            offline_equipment_item = OfflineEquipmentDto.from_dict(offline_equipment_item_data)

            offline_equipment.append(offline_equipment_item)

        kpi_count = d.pop("kpiCount", UNSET)

        sensor_count = d.pop("sensorCount", UNSET)

        offline_sensor_count = d.pop("offlineSensorCount", UNSET)

        online_sensor_count = d.pop("onlineSensorCount", UNSET)

        has_draft_samplings = d.pop("hasDraftSamplings", UNSET)

        process_dto = cls(
            name=name,
            id=id,
            description=description,
            update_date=update_date,
            creation_date=creation_date,
            gmp_enabled=gmp_enabled,
            start_date=start_date,
            end_date=end_date,
            status=status,
            publish_enabled=publish_enabled,
            publish_planned_at=publish_planned_at,
            imported=imported,
            import_date=import_date,
            last_usage_date=last_usage_date,
            simulated=simulated,
            python_engine_status=python_engine_status,
            type=type,
            control_recipe_id=control_recipe_id,
            control_recipe_name=control_recipe_name,
            warm_up_date=warm_up_date,
            python_online_calculator_restart_date=python_online_calculator_restart_date,
            python_sampling_calculator_restart_date=python_sampling_calculator_restart_date,
            media=media,
            buffer=buffer,
            process_archive_transition_status=process_archive_transition_status,
            current_phase=current_phase,
            online_equipment=online_equipment,
            offline_equipment=offline_equipment,
            kpi_count=kpi_count,
            sensor_count=sensor_count,
            offline_sensor_count=offline_sensor_count,
            online_sensor_count=online_sensor_count,
            has_draft_samplings=has_draft_samplings,
        )

        process_dto.additional_properties = d
        return process_dto

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
