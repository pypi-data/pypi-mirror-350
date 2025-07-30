from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.abstract_computable_model_dto_calculation_style import AbstractComputableModelDtoCalculationStyle
from ..models.abstract_computable_model_dto_engine_type import AbstractComputableModelDtoEngineType
from ..models.abstract_computable_model_dto_status import AbstractComputableModelDtoStatus
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.computable_model_input_dto import ComputableModelInputDto
    from ..models.computable_model_output_dto import ComputableModelOutputDto
    from ..models.sensor_type_dto import SensorTypeDto


T = TypeVar("T", bound="JythonComputableModelDto")


@_attrs_define
class JythonComputableModelDto:
    """
    Attributes:
        engine_type (AbstractComputableModelDtoEngineType):
        kpi_name (str):
        abbr (str):
        calculation_style (AbstractComputableModelDtoCalculationStyle):
        outputs (List['ComputableModelOutputDto']):
        id (Union[Unset, int]):
        sensor_type (Union[Unset, SensorTypeDto]):
        inputs (Union[Unset, List['ComputableModelInputDto']]):
        status (Union[Unset, AbstractComputableModelDtoStatus]):
        description (Union[Unset, str]):
        creation_date (Union[Unset, int]):
        update_date (Union[Unset, int]):
        script (Union[Unset, str]):
    """

    engine_type: AbstractComputableModelDtoEngineType
    kpi_name: str
    abbr: str
    calculation_style: AbstractComputableModelDtoCalculationStyle
    outputs: List["ComputableModelOutputDto"]
    id: Union[Unset, int] = UNSET
    sensor_type: Union[Unset, "SensorTypeDto"] = UNSET
    inputs: Union[Unset, List["ComputableModelInputDto"]] = UNSET
    status: Union[Unset, AbstractComputableModelDtoStatus] = UNSET
    description: Union[Unset, str] = UNSET
    creation_date: Union[Unset, int] = UNSET
    update_date: Union[Unset, int] = UNSET
    script: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        engine_type = self.engine_type.value

        kpi_name = self.kpi_name

        abbr = self.abbr

        calculation_style = self.calculation_style.value

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item = outputs_item_data.to_dict()
            outputs.append(outputs_item)

        id = self.id

        sensor_type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sensor_type, Unset):
            sensor_type = self.sensor_type.to_dict()

        inputs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inputs, Unset):
            inputs = []
            for inputs_item_data in self.inputs:
                inputs_item = inputs_item_data.to_dict()
                inputs.append(inputs_item)

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        description = self.description

        creation_date = self.creation_date

        update_date = self.update_date

        script = self.script

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engineType": engine_type,
                "kpiName": kpi_name,
                "abbr": abbr,
                "calculationStyle": calculation_style,
                "outputs": outputs,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if sensor_type is not UNSET:
            field_dict["sensorType"] = sensor_type
        if inputs is not UNSET:
            field_dict["inputs"] = inputs
        if status is not UNSET:
            field_dict["status"] = status
        if description is not UNSET:
            field_dict["description"] = description
        if creation_date is not UNSET:
            field_dict["creationDate"] = creation_date
        if update_date is not UNSET:
            field_dict["updateDate"] = update_date
        if script is not UNSET:
            field_dict["script"] = script

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.computable_model_input_dto import ComputableModelInputDto
        from ..models.computable_model_output_dto import ComputableModelOutputDto
        from ..models.sensor_type_dto import SensorTypeDto

        d = src_dict.copy()
        engine_type = AbstractComputableModelDtoEngineType(d.pop("engineType"))

        kpi_name = d.pop("kpiName")

        abbr = d.pop("abbr")

        calculation_style = AbstractComputableModelDtoCalculationStyle(d.pop("calculationStyle"))

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:
            outputs_item = ComputableModelOutputDto.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        id = d.pop("id", UNSET)

        _sensor_type = d.pop("sensorType", UNSET)
        sensor_type: Union[Unset, SensorTypeDto]
        if isinstance(_sensor_type, Unset):
            sensor_type = UNSET
        else:
            sensor_type = SensorTypeDto.from_dict(_sensor_type)

        inputs = []
        _inputs = d.pop("inputs", UNSET)
        for inputs_item_data in _inputs or []:
            inputs_item = ComputableModelInputDto.from_dict(inputs_item_data)

            inputs.append(inputs_item)

        _status = d.pop("status", UNSET)
        status: Union[Unset, AbstractComputableModelDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = AbstractComputableModelDtoStatus(_status)

        description = d.pop("description", UNSET)

        creation_date = d.pop("creationDate", UNSET)

        update_date = d.pop("updateDate", UNSET)

        script = d.pop("script", UNSET)

        jython_computable_model_dto = cls(
            engine_type=engine_type,
            kpi_name=kpi_name,
            abbr=abbr,
            calculation_style=calculation_style,
            outputs=outputs,
            id=id,
            sensor_type=sensor_type,
            inputs=inputs,
            status=status,
            description=description,
            creation_date=creation_date,
            update_date=update_date,
            script=script,
        )

        jython_computable_model_dto.additional_properties = d
        return jython_computable_model_dto

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
