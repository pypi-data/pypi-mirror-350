from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.minimum_process_group_dto_status import MinimumProcessGroupDtoStatus
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.minimum_process_dto import MinimumProcessDto
    from ..models.online_equipment_dto import OnlineEquipmentDto


T = TypeVar("T", bound="MinimumProcessGroupDto")


@_attrs_define
class MinimumProcessGroupDto:
    """
    Attributes:
        name (str):
        id (Union[Unset, int]):
        creation_date (Union[Unset, int]):
        last_usage_date (Union[Unset, int]):
        part_of_experiment_equipment_group (Union[Unset, OnlineEquipmentDto]):
        update_date (Union[Unset, int]):
        manually_created (Union[Unset, bool]):
        has_charts (Union[Unset, bool]):
        status (Union[Unset, MinimumProcessGroupDtoStatus]):
        processes (Union[Unset, List['MinimumProcessDto']]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    creation_date: Union[Unset, int] = UNSET
    last_usage_date: Union[Unset, int] = UNSET
    part_of_experiment_equipment_group: Union[Unset, "OnlineEquipmentDto"] = UNSET
    update_date: Union[Unset, int] = UNSET
    manually_created: Union[Unset, bool] = UNSET
    has_charts: Union[Unset, bool] = UNSET
    status: Union[Unset, MinimumProcessGroupDtoStatus] = UNSET
    processes: Union[Unset, List["MinimumProcessDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        id = self.id

        creation_date = self.creation_date

        last_usage_date = self.last_usage_date

        part_of_experiment_equipment_group: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.part_of_experiment_equipment_group, Unset):
            part_of_experiment_equipment_group = self.part_of_experiment_equipment_group.to_dict()

        update_date = self.update_date

        manually_created = self.manually_created

        has_charts = self.has_charts

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        processes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.processes, Unset):
            processes = []
            for processes_item_data in self.processes:
                processes_item = processes_item_data.to_dict()
                processes.append(processes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if last_usage_date is not UNSET:
            field_dict["lastUsageDate"] = last_usage_date
        if part_of_experiment_equipment_group is not UNSET:
            field_dict["partOfExperimentEquipmentGroup"] = part_of_experiment_equipment_group
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date
        if manually_created is not UNSET:
            field_dict["manuallyCreated"] = manually_created
        if has_charts is not UNSET:
            field_dict["hasCharts"] = has_charts
        if status is not UNSET:
            field_dict["status"] = status
        if processes is not UNSET:
            field_dict["processes"] = processes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.minimum_process_dto import MinimumProcessDto
        from ..models.online_equipment_dto import OnlineEquipmentDto

        d = src_dict.copy()
        name = d.pop("name")

        id = d.pop("id", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        last_usage_date = d.pop("lastUsageDate", UNSET)

        _part_of_experiment_equipment_group = d.pop("partOfExperimentEquipmentGroup", UNSET)
        part_of_experiment_equipment_group: Union[Unset, OnlineEquipmentDto]
        if isinstance(_part_of_experiment_equipment_group, Unset):
            part_of_experiment_equipment_group = UNSET
        else:
            part_of_experiment_equipment_group = OnlineEquipmentDto.from_dict(_part_of_experiment_equipment_group)

        update_date = d.pop("updateDate", UNSET)

        manually_created = d.pop("manuallyCreated", UNSET)

        has_charts = d.pop("hasCharts", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, MinimumProcessGroupDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = MinimumProcessGroupDtoStatus(_status)

        processes = []
        _processes = d.pop("processes", UNSET)
        for processes_item_data in _processes or []:
            processes_item = MinimumProcessDto.from_dict(processes_item_data)

            processes.append(processes_item)

        minimum_process_group_dto = cls(
            name=name,
            id=id,
            creation_date=creation_date,
            last_usage_date=last_usage_date,
            part_of_experiment_equipment_group=part_of_experiment_equipment_group,
            update_date=update_date,
            manually_created=manually_created,
            has_charts=has_charts,
            status=status,
            processes=processes,
        )

        minimum_process_group_dto.additional_properties = d
        return minimum_process_group_dto

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
