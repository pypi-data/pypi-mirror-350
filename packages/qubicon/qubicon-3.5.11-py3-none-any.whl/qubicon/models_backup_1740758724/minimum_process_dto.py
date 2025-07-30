from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.minimum_process_dto_python_engine_status import MinimumProcessDtoPythonEngineStatus
from ..models.minimum_process_dto_status import MinimumProcessDtoStatus
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="MinimumProcessDto")


@_attrs_define
class MinimumProcessDto:
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
        status (Union[Unset, MinimumProcessDtoStatus]):
        publish_enabled (Union[Unset, bool]):
        publish_planned_at (Union[Unset, int]):
        imported (Union[Unset, bool]):
        import_date (Union[Unset, int]):
        last_usage_date (Union[Unset, int]):
        simulated (Union[Unset, bool]):
        python_engine_status (Union[Unset, MinimumProcessDtoPythonEngineStatus]):
    """

    name: str
    id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    update_date: Union[Unset, int] = UNSET
    creation_date: Union[Unset, int] = UNSET
    gmp_enabled: Union[Unset, bool] = UNSET
    start_date: Union[Unset, int] = UNSET
    end_date: Union[Unset, int] = UNSET
    status: Union[Unset, MinimumProcessDtoStatus] = UNSET
    publish_enabled: Union[Unset, bool] = UNSET
    publish_planned_at: Union[Unset, int] = UNSET
    imported: Union[Unset, bool] = UNSET
    import_date: Union[Unset, int] = UNSET
    last_usage_date: Union[Unset, int] = UNSET
    simulated: Union[Unset, bool] = UNSET
    python_engine_status: Union[Unset, MinimumProcessDtoPythonEngineStatus] = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
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
        status: Union[Unset, MinimumProcessDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = MinimumProcessDtoStatus(_status)

        publish_enabled = d.pop("publishEnabled", UNSET)

        publish_planned_at = d.pop("publishPlannedAt", UNSET)

        imported = d.pop("imported", UNSET)

        import_date = d.pop("importDate", UNSET)

        last_usage_date = d.pop("lastUsageDate", UNSET)

        simulated = d.pop("simulated", UNSET)

        _python_engine_status = d.pop("pythonEngineStatus", UNSET)
        python_engine_status: Union[Unset, MinimumProcessDtoPythonEngineStatus]
        if isinstance(_python_engine_status, Unset):
            python_engine_status = UNSET
        else:
            python_engine_status = MinimumProcessDtoPythonEngineStatus(_python_engine_status)

        minimum_process_dto = cls(
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
        )

        minimum_process_dto.additional_properties = d
        return minimum_process_dto

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
