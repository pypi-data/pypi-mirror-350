from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.channel_dto_data_presentation_type import ChannelDtoDataPresentationType
from ..models.channel_dto_node_type import ChannelDtoNodeType
from ..models.channel_dto_type import ChannelDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto


T = TypeVar("T", bound="ChannelDto")


@_attrs_define
class ChannelDto:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        equipment_label (Union[Unset, str]):
        kpi_model_label (Union[Unset, str]):
        type (Union[Unset, ChannelDtoType]):
        node_type (Union[Unset, ChannelDtoNodeType]):
        physical_quantity_unit (Union[Unset, PhysicalQuantityUnitDto]):
        data_presentation_type (Union[Unset, ChannelDtoDataPresentationType]):
        equipment_name (Union[Unset, str]):
        imported (Union[Unset, bool]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    equipment_label: Union[Unset, str] = UNSET
    kpi_model_label: Union[Unset, str] = UNSET
    type: Union[Unset, ChannelDtoType] = UNSET
    node_type: Union[Unset, ChannelDtoNodeType] = UNSET
    physical_quantity_unit: Union[Unset, "PhysicalQuantityUnitDto"] = UNSET
    data_presentation_type: Union[Unset, ChannelDtoDataPresentationType] = UNSET
    equipment_name: Union[Unset, str] = UNSET
    imported: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        equipment_label = self.equipment_label

        kpi_model_label = self.kpi_model_label

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        node_type: Union[Unset, str] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value

        physical_quantity_unit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.physical_quantity_unit, Unset):
            physical_quantity_unit = self.physical_quantity_unit.to_dict()

        data_presentation_type: Union[Unset, str] = UNSET
        if not isinstance(self.data_presentation_type, Unset):
            data_presentation_type = self.data_presentation_type.value

        equipment_name = self.equipment_name

        imported = self.imported

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if equipment_label is not UNSET:
            field_dict["equipmentLabel"] = equipment_label
        if kpi_model_label is not UNSET:
            field_dict["kpiModelLabel"] = kpi_model_label
        if type is not UNSET:
            field_dict["type"] = type
        if node_type is not UNSET:
            field_dict["nodeType"] = node_type
        if physical_quantity_unit is not UNSET:
            field_dict["physicalQuantityUnit"] = physical_quantity_unit
        if data_presentation_type is not UNSET:
            field_dict["dataPresentationType"] = data_presentation_type
        if equipment_name is not UNSET:
            field_dict["equipmentName"] = equipment_name
        if imported is not UNSET:
            field_dict["imported"] = imported

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.physical_quantity_unit_dto import PhysicalQuantityUnitDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        equipment_label = d.pop("equipmentLabel", UNSET)

        kpi_model_label = d.pop("kpiModelLabel", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ChannelDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ChannelDtoType(_type)

        _node_type = d.pop("nodeType", UNSET)
        node_type: Union[Unset, ChannelDtoNodeType]
        if isinstance(_node_type, Unset):
            node_type = UNSET
        else:
            node_type = ChannelDtoNodeType(_node_type)

        _physical_quantity_unit = d.pop("physicalQuantityUnit", UNSET)
        physical_quantity_unit: Union[Unset, PhysicalQuantityUnitDto]
        if isinstance(_physical_quantity_unit, Unset):
            physical_quantity_unit = UNSET
        else:
            physical_quantity_unit = PhysicalQuantityUnitDto.from_dict(_physical_quantity_unit)

        _data_presentation_type = d.pop("dataPresentationType", UNSET)
        data_presentation_type: Union[Unset, ChannelDtoDataPresentationType]
        if isinstance(_data_presentation_type, Unset):
            data_presentation_type = UNSET
        else:
            data_presentation_type = ChannelDtoDataPresentationType(_data_presentation_type)

        equipment_name = d.pop("equipmentName", UNSET)

        imported = d.pop("imported", UNSET)

        channel_dto = cls(
            id=id,
            name=name,
            equipment_label=equipment_label,
            kpi_model_label=kpi_model_label,
            type=type,
            node_type=node_type,
            physical_quantity_unit=physical_quantity_unit,
            data_presentation_type=data_presentation_type,
            equipment_name=equipment_name,
            imported=imported,
        )

        channel_dto.additional_properties = d
        return channel_dto

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
