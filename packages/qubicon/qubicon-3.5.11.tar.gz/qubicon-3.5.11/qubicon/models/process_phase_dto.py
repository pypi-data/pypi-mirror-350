from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.process_phase_dto_status import ProcessPhaseDtoStatus
from ..models.process_phase_dto_type import ProcessPhaseDtoType
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="ProcessPhaseDto")


@_attrs_define
class ProcessPhaseDto:
    """
    Attributes:
        id (Union[Unset, int]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        order (Union[Unset, int]):
        status (Union[Unset, ProcessPhaseDtoStatus]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        type (Union[Unset, ProcessPhaseDtoType]):
        duration_min_ms (Union[Unset, int]):
        duration_max_ms (Union[Unset, int]):
        recipe_phase_id (Union[Unset, int]):
    """

    id: Union[Unset, int] = UNSET
    start_date: Union[Unset, int] = UNSET
    end_date: Union[Unset, int] = UNSET
    order: Union[Unset, int] = UNSET
    status: Union[Unset, ProcessPhaseDtoStatus] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type: Union[Unset, ProcessPhaseDtoType] = UNSET
    duration_min_ms: Union[Unset, int] = UNSET
    duration_max_ms: Union[Unset, int] = UNSET
    recipe_phase_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        start_date = self.start_date

        end_date = self.end_date

        order = self.order

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        name = self.name

        description = self.description

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        duration_min_ms = self.duration_min_ms

        duration_max_ms = self.duration_max_ms

        recipe_phase_id = self.recipe_phase_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if order is not UNSET:
            field_dict["order"] = order
        if status is not UNSET:
            field_dict["status"] = status
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if type is not UNSET:
            field_dict["type"] = type
        if duration_min_ms is not UNSET:
            field_dict["durationMinMs"] = duration_min_ms
        if duration_max_ms is not UNSET:
            field_dict["durationMaxMs"] = duration_max_ms
        if recipe_phase_id is not UNSET:
            field_dict["recipePhaseId"] = recipe_phase_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        start_date = d.pop("startDate", UNSET)

        end_date = d.pop("endDate", UNSET)

        order = d.pop("order", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ProcessPhaseDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ProcessPhaseDtoStatus(_status)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ProcessPhaseDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ProcessPhaseDtoType(_type)

        duration_min_ms = d.pop("durationMinMs", UNSET)

        duration_max_ms = d.pop("durationMaxMs", UNSET)

        recipe_phase_id = d.pop("recipePhaseId", UNSET)

        process_phase_dto = cls(
            id=id,
            start_date=start_date,
            end_date=end_date,
            order=order,
            status=status,
            name=name,
            description=description,
            type=type,
            duration_min_ms=duration_min_ms,
            duration_max_ms=duration_max_ms,
            recipe_phase_id=recipe_phase_id,
        )

        process_phase_dto.additional_properties = d
        return process_phase_dto

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
