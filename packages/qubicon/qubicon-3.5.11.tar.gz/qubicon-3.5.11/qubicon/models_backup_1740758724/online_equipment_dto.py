from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.online_equipment_dto_equipment_data_refresh_status import OnlineEquipmentDtoEquipmentDataRefreshStatus
from ..models.online_equipment_dto_equipment_metadata_rescan_status import (
    OnlineEquipmentDtoEquipmentMetadataRescanStatus,
)
from ..models.online_equipment_dto_status import OnlineEquipmentDtoStatus
from ..models.online_equipment_dto_type import OnlineEquipmentDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gmp_track_dto import GmpTrackDto
    from ..models.online_equipment_node_object_dto import OnlineEquipmentNodeObjectDto


T = TypeVar("T", bound="OnlineEquipmentDto")


@_attrs_define
class OnlineEquipmentDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        status (Union[Unset, OnlineEquipmentDtoStatus]):
        gmp_enabled (Union[Unset, bool]):
        polling_mode (Union[Unset, bool]):
        simulated (Union[Unset, bool]):
        standalone (Union[Unset, bool]):
        uses_new_connection (Union[Unset, bool]):
        auto_created (Union[Unset, bool]):
        master_equipment_ids (Union[Unset, List[int]]):
        last_connection_check_status (Union[Unset, bool]):
        last_connection_check_date (Union[Unset, int]):
        last_connection_check_error (Union[Unset, str]):
        opc_ua_root_node (Union[Unset, OnlineEquipmentNodeObjectDto]):
        parent_id (Union[Unset, int]):
        parent_name (Union[Unset, str]):
        server_id (Union[Unset, int]):
        server_name (Union[Unset, str]):
        health_opc_ua_node_id (Union[Unset, str]):
        read_frequency_ms (Union[Unset, int]):
        read_subscription_sampling_interval (Union[Unset, int]):
        read_subscription_publishing_interval (Union[Unset, int]):
        read_subscription_queue_size (Union[Unset, int]):
        gmp_track (Union[Unset, GmpTrackDto]):
        version_group_first_id (Union[Unset, int]):
        version_group_copied_from_id (Union[Unset, int]):
        version_group_version (Union[Unset, int]):
        type (Union[Unset, OnlineEquipmentDtoType]):
        equipment_data_refresh_status (Union[Unset, OnlineEquipmentDtoEquipmentDataRefreshStatus]):
        equipment_data_refresh_started (Union[Unset, int]):
        equipment_data_refresh_completed (Union[Unset, int]):
        equipment_data_refresh_progress (Union[Unset, int]):
        equipment_metadata_rescan_status (Union[Unset, OnlineEquipmentDtoEquipmentMetadataRescanStatus]):
        equipment_metadata_rescan_started (Union[Unset, int]):
        equipment_metadata_rescan_completed (Union[Unset, int]):
        equipment_metadata_rescan_progress (Union[Unset, int]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    status: Union[Unset, OnlineEquipmentDtoStatus] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    polling_mode: Union[Unset, bool] = UNSET
    simulated: Union[Unset, bool] = UNSET
    standalone: Union[Unset, bool] = UNSET
    uses_new_connection: Union[Unset, bool] = UNSET
    auto_created: Union[Unset, bool] = UNSET
    master_equipment_ids: Union[Unset, List[int]] = UNSET
    last_connection_check_status: Union[Unset, bool] = UNSET
    last_connection_check_date: Union[Unset, int] = UNSET
    last_connection_check_error: Union[Unset, str] = UNSET
    opc_ua_root_node: Union[Unset, "OnlineEquipmentNodeObjectDto"] = UNSET
    parent_id: Union[Unset, int] = UNSET
    parent_name: Union[Unset, str] = UNSET
    server_id: Union[Unset, int] = UNSET
    server_name: Union[Unset, str] = UNSET
    health_opc_ua_node_id: Union[Unset, str] = UNSET
    read_frequency_ms: Union[Unset, int] = UNSET
    read_subscription_sampling_interval: Union[Unset, int] = UNSET
    read_subscription_publishing_interval: Union[Unset, int] = UNSET
    read_subscription_queue_size: Union[Unset, int] = UNSET
    gmp_track: Union[Unset, "GmpTrackDto"] = UNSET
    version_group_first_id: Union[Unset, int] = UNSET
    version_group_copied_from_id: Union[Unset, int] = UNSET
    version_group_version: Union[Unset, int] = UNSET
    type: Union[Unset, OnlineEquipmentDtoType] = UNSET
    equipment_data_refresh_status: Union[Unset, OnlineEquipmentDtoEquipmentDataRefreshStatus] = UNSET
    equipment_data_refresh_started: Union[Unset, int] = UNSET
    equipment_data_refresh_completed: Union[Unset, int] = UNSET
    equipment_data_refresh_progress: Union[Unset, int] = UNSET
    equipment_metadata_rescan_status: Union[Unset, OnlineEquipmentDtoEquipmentMetadataRescanStatus] = UNSET
    equipment_metadata_rescan_started: Union[Unset, int] = UNSET
    equipment_metadata_rescan_completed: Union[Unset, int] = UNSET
    equipment_metadata_rescan_progress: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        gmp_enabled = self.gmp_enabled

        polling_mode = self.polling_mode

        simulated = self.simulated

        standalone = self.standalone

        uses_new_connection = self.uses_new_connection

        auto_created = self.auto_created

        master_equipment_ids: Union[Unset, List[int]] = UNSET
        if not isinstance(self.master_equipment_ids, Unset):
            master_equipment_ids = self.master_equipment_ids

        last_connection_check_status = self.last_connection_check_status

        last_connection_check_date = self.last_connection_check_date

        last_connection_check_error = self.last_connection_check_error

        opc_ua_root_node: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.opc_ua_root_node, Unset):
            opc_ua_root_node = self.opc_ua_root_node.to_dict()

        parent_id = self.parent_id

        parent_name = self.parent_name

        server_id = self.server_id

        server_name = self.server_name

        health_opc_ua_node_id = self.health_opc_ua_node_id

        read_frequency_ms = self.read_frequency_ms

        read_subscription_sampling_interval = self.read_subscription_sampling_interval

        read_subscription_publishing_interval = self.read_subscription_publishing_interval

        read_subscription_queue_size = self.read_subscription_queue_size

        gmp_track: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.gmp_track, Unset):
            gmp_track = self.gmp_track.to_dict()

        version_group_first_id = self.version_group_first_id

        version_group_copied_from_id = self.version_group_copied_from_id

        version_group_version = self.version_group_version

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        equipment_data_refresh_status: Union[Unset, str] = UNSET
        if not isinstance(self.equipment_data_refresh_status, Unset):
            equipment_data_refresh_status = self.equipment_data_refresh_status.value

        equipment_data_refresh_started = self.equipment_data_refresh_started

        equipment_data_refresh_completed = self.equipment_data_refresh_completed

        equipment_data_refresh_progress = self.equipment_data_refresh_progress

        equipment_metadata_rescan_status: Union[Unset, str] = UNSET
        if not isinstance(self.equipment_metadata_rescan_status, Unset):
            equipment_metadata_rescan_status = self.equipment_metadata_rescan_status.value

        equipment_metadata_rescan_started = self.equipment_metadata_rescan_started

        equipment_metadata_rescan_completed = self.equipment_metadata_rescan_completed

        equipment_metadata_rescan_progress = self.equipment_metadata_rescan_progress

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if gmp_enabled is not UNSET:
            field_dict["gmpEnabled"] = gmp_enabled
        if polling_mode is not UNSET:
            field_dict["pollingMode"] = polling_mode
        if simulated is not UNSET:
            field_dict["simulated"] = simulated
        if standalone is not UNSET:
            field_dict["standalone"] = standalone
        if uses_new_connection is not UNSET:
            field_dict["usesNewConnection"] = uses_new_connection
        if auto_created is not UNSET:
            field_dict["autoCreated"] = auto_created
        if master_equipment_ids is not UNSET:
            field_dict["masterEquipmentIds"] = master_equipment_ids
        if last_connection_check_status is not UNSET:
            field_dict["lastConnectionCheckStatus"] = last_connection_check_status
        if last_connection_check_date is not UNSET:
            field_dict["lastConnectionCheckDate"] = last_connection_check_date
        if last_connection_check_error is not UNSET:
            field_dict["lastConnectionCheckError"] = last_connection_check_error
        if opc_ua_root_node is not UNSET:
            field_dict["opcUaRootNode"] = opc_ua_root_node
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if parent_name is not UNSET:
            field_dict["parentName"] = parent_name
        if server_id is not UNSET:
            field_dict["serverId"] = server_id
        if server_name is not UNSET:
            field_dict["serverName"] = server_name
        if health_opc_ua_node_id is not UNSET:
            field_dict["healthOpcUaNodeId"] = health_opc_ua_node_id
        if read_frequency_ms is not UNSET:
            field_dict["readFrequencyMs"] = read_frequency_ms
        if read_subscription_sampling_interval is not UNSET:
            field_dict["readSubscriptionSamplingInterval"] = read_subscription_sampling_interval
        if read_subscription_publishing_interval is not UNSET:
            field_dict["readSubscriptionPublishingInterval"] = read_subscription_publishing_interval
        if read_subscription_queue_size is not UNSET:
            field_dict["readSubscriptionQueueSize"] = read_subscription_queue_size
        if gmp_track is not UNSET:
            field_dict["gmpTrack"] = gmp_track
        if version_group_first_id is not UNSET:
            field_dict["versionGroupFirstId"] = version_group_first_id
        if version_group_copied_from_id is not UNSET:
            field_dict["versionGroupCopiedFromId"] = version_group_copied_from_id
        if version_group_version is not UNSET:
            field_dict["versionGroupVersion"] = version_group_version
        if type is not UNSET:
            field_dict["type"] = type
        if equipment_data_refresh_status is not UNSET:
            field_dict["equipmentDataRefreshStatus"] = equipment_data_refresh_status
        if equipment_data_refresh_started is not UNSET:
            field_dict["equipmentDataRefreshStarted"] = equipment_data_refresh_started
        if equipment_data_refresh_completed is not UNSET:
            field_dict["equipmentDataRefreshCompleted"] = equipment_data_refresh_completed
        if equipment_data_refresh_progress is not UNSET:
            field_dict["equipmentDataRefreshProgress"] = equipment_data_refresh_progress
        if equipment_metadata_rescan_status is not UNSET:
            field_dict["equipmentMetadataRescanStatus"] = equipment_metadata_rescan_status
        if equipment_metadata_rescan_started is not UNSET:
            field_dict["equipmentMetadataRescanStarted"] = equipment_metadata_rescan_started
        if equipment_metadata_rescan_completed is not UNSET:
            field_dict["equipmentMetadataRescanCompleted"] = equipment_metadata_rescan_completed
        if equipment_metadata_rescan_progress is not UNSET:
            field_dict["equipmentMetadataRescanProgress"] = equipment_metadata_rescan_progress

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.gmp_track_dto import GmpTrackDto
        from ..models.online_equipment_node_object_dto import OnlineEquipmentNodeObjectDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, OnlineEquipmentDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = OnlineEquipmentDtoStatus(_status)

        gmp_enabled = d.pop("gmpEnabled", UNSET)

        polling_mode = d.pop("pollingMode", UNSET)

        simulated = d.pop("simulated", UNSET)

        standalone = d.pop("standalone", UNSET)

        uses_new_connection = d.pop("usesNewConnection", UNSET)

        auto_created = d.pop("autoCreated", UNSET)

        master_equipment_ids = cast(List[int], d.pop("masterEquipmentIds", UNSET))

        last_connection_check_status = d.pop("lastConnectionCheckStatus", UNSET)

        last_connection_check_date = d.pop("lastConnectionCheckDate", UNSET)

        last_connection_check_error = d.pop("lastConnectionCheckError", UNSET)

        _opc_ua_root_node = d.pop("opcUaRootNode", UNSET)
        opc_ua_root_node: Union[Unset, OnlineEquipmentNodeObjectDto]
        if isinstance(_opc_ua_root_node, Unset):
            opc_ua_root_node = UNSET
        else:
            opc_ua_root_node = OnlineEquipmentNodeObjectDto.from_dict(_opc_ua_root_node)

        parent_id = d.pop("parentId", UNSET)

        parent_name = d.pop("parentName", UNSET)

        server_id = d.pop("serverId", UNSET)

        server_name = d.pop("serverName", UNSET)

        health_opc_ua_node_id = d.pop("healthOpcUaNodeId", UNSET)

        read_frequency_ms = d.pop("readFrequencyMs", UNSET)

        read_subscription_sampling_interval = d.pop("readSubscriptionSamplingInterval", UNSET)

        read_subscription_publishing_interval = d.pop("readSubscriptionPublishingInterval", UNSET)

        read_subscription_queue_size = d.pop("readSubscriptionQueueSize", UNSET)

        _gmp_track = d.pop("gmpTrack", UNSET)
        gmp_track: Union[Unset, GmpTrackDto]
        if isinstance(_gmp_track, Unset):
            gmp_track = UNSET
        else:
            gmp_track = GmpTrackDto.from_dict(_gmp_track)

        version_group_first_id = d.pop("versionGroupFirstId", UNSET)

        version_group_copied_from_id = d.pop("versionGroupCopiedFromId", UNSET)

        version_group_version = d.pop("versionGroupVersion", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, OnlineEquipmentDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = OnlineEquipmentDtoType(_type)

        _equipment_data_refresh_status = d.pop("equipmentDataRefreshStatus", UNSET)
        equipment_data_refresh_status: Union[Unset, OnlineEquipmentDtoEquipmentDataRefreshStatus]
        if isinstance(_equipment_data_refresh_status, Unset):
            equipment_data_refresh_status = UNSET
        else:
            equipment_data_refresh_status = OnlineEquipmentDtoEquipmentDataRefreshStatus(_equipment_data_refresh_status)

        equipment_data_refresh_started = d.pop("equipmentDataRefreshStarted", UNSET)

        equipment_data_refresh_completed = d.pop("equipmentDataRefreshCompleted", UNSET)

        equipment_data_refresh_progress = d.pop("equipmentDataRefreshProgress", UNSET)

        _equipment_metadata_rescan_status = d.pop("equipmentMetadataRescanStatus", UNSET)
        equipment_metadata_rescan_status: Union[Unset, OnlineEquipmentDtoEquipmentMetadataRescanStatus]
        if isinstance(_equipment_metadata_rescan_status, Unset):
            equipment_metadata_rescan_status = UNSET
        else:
            equipment_metadata_rescan_status = OnlineEquipmentDtoEquipmentMetadataRescanStatus(
                _equipment_metadata_rescan_status
            )

        equipment_metadata_rescan_started = d.pop("equipmentMetadataRescanStarted", UNSET)

        equipment_metadata_rescan_completed = d.pop("equipmentMetadataRescanCompleted", UNSET)

        equipment_metadata_rescan_progress = d.pop("equipmentMetadataRescanProgress", UNSET)

        online_equipment_dto = cls(
            name=name,
            id=id,
            status=status,
            gmp_enabled=gmp_enabled,
            polling_mode=polling_mode,
            simulated=simulated,
            standalone=standalone,
            uses_new_connection=uses_new_connection,
            auto_created=auto_created,
            master_equipment_ids=master_equipment_ids,
            last_connection_check_status=last_connection_check_status,
            last_connection_check_date=last_connection_check_date,
            last_connection_check_error=last_connection_check_error,
            opc_ua_root_node=opc_ua_root_node,
            parent_id=parent_id,
            parent_name=parent_name,
            server_id=server_id,
            server_name=server_name,
            health_opc_ua_node_id=health_opc_ua_node_id,
            read_frequency_ms=read_frequency_ms,
            read_subscription_sampling_interval=read_subscription_sampling_interval,
            read_subscription_publishing_interval=read_subscription_publishing_interval,
            read_subscription_queue_size=read_subscription_queue_size,
            gmp_track=gmp_track,
            version_group_first_id=version_group_first_id,
            version_group_copied_from_id=version_group_copied_from_id,
            version_group_version=version_group_version,
            type=type,
            equipment_data_refresh_status=equipment_data_refresh_status,
            equipment_data_refresh_started=equipment_data_refresh_started,
            equipment_data_refresh_completed=equipment_data_refresh_completed,
            equipment_data_refresh_progress=equipment_data_refresh_progress,
            equipment_metadata_rescan_status=equipment_metadata_rescan_status,
            equipment_metadata_rescan_started=equipment_metadata_rescan_started,
            equipment_metadata_rescan_completed=equipment_metadata_rescan_completed,
            equipment_metadata_rescan_progress=equipment_metadata_rescan_progress,
        )

        online_equipment_dto.additional_properties = d
        return online_equipment_dto

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
