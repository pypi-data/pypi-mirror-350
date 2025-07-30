from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.publish_schema_dto_db_column_type import PublishSchemaDtoDbColumnType
from ..models.publish_schema_dto_field_data_type import PublishSchemaDtoFieldDataType
from qubicon.api.types import UNSET, Unset

T = TypeVar("T", bound="PublishSchemaDto")


@_attrs_define
class PublishSchemaDto:
    """
    Attributes:
        id (Union[Unset, int]):
        process_scheme (Union[Unset, str]):
        sub_process (Union[Unset, str]):
        process_step (Union[Unset, str]):
        field_name (Union[Unset, str]):
        field_unit (Union[Unset, str]):
        field_order (Union[Unset, int]):
        field_data_type (Union[Unset, PublishSchemaDtoFieldDataType]):
        process_step_type (Union[Unset, str]):
        db_column_name (Union[Unset, str]):
        db_column_type (Union[Unset, PublishSchemaDtoDbColumnType]):
    """

    id: Union[Unset, int] = UNSET
    process_scheme: Union[Unset, str] = UNSET
    sub_process: Union[Unset, str] = UNSET
    process_step: Union[Unset, str] = UNSET
    field_name: Union[Unset, str] = UNSET
    field_unit: Union[Unset, str] = UNSET
    field_order: Union[Unset, int] = UNSET
    field_data_type: Union[Unset, PublishSchemaDtoFieldDataType] = UNSET
    process_step_type: Union[Unset, str] = UNSET
    db_column_name: Union[Unset, str] = UNSET
    db_column_type: Union[Unset, PublishSchemaDtoDbColumnType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        process_scheme = self.process_scheme

        sub_process = self.sub_process

        process_step = self.process_step

        field_name = self.field_name

        field_unit = self.field_unit

        field_order = self.field_order

        field_data_type: Union[Unset, str] = UNSET
        if not isinstance(self.field_data_type, Unset):
            field_data_type = self.field_data_type.value

        process_step_type = self.process_step_type

        db_column_name = self.db_column_name

        db_column_type: Union[Unset, str] = UNSET
        if not isinstance(self.db_column_type, Unset):
            db_column_type = self.db_column_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if process_scheme is not UNSET:
            field_dict["processScheme"] = process_scheme
        if sub_process is not UNSET:
            field_dict["subProcess"] = sub_process
        if process_step is not UNSET:
            field_dict["processStep"] = process_step
        if field_name is not UNSET:
            field_dict["fieldName"] = field_name
        if field_unit is not UNSET:
            field_dict["fieldUnit"] = field_unit
        if field_order is not UNSET:
            field_dict["fieldOrder"] = field_order
        if field_data_type is not UNSET:
            field_dict["fieldDataType"] = field_data_type
        if process_step_type is not UNSET:
            field_dict["processStepType"] = process_step_type
        if db_column_name is not UNSET:
            field_dict["dbColumnName"] = db_column_name
        if db_column_type is not UNSET:
            field_dict["dbColumnType"] = db_column_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        process_scheme = d.pop("processScheme", UNSET)

        sub_process = d.pop("subProcess", UNSET)

        process_step = d.pop("processStep", UNSET)

        field_name = d.pop("fieldName", UNSET)

        field_unit = d.pop("fieldUnit", UNSET)

        field_order = d.pop("fieldOrder", UNSET)

        _field_data_type = d.pop("fieldDataType", UNSET)
        field_data_type: Union[Unset, PublishSchemaDtoFieldDataType]
        if isinstance(_field_data_type, Unset):
            field_data_type = UNSET
        else:
            field_data_type = PublishSchemaDtoFieldDataType(_field_data_type)

        process_step_type = d.pop("processStepType", UNSET)

        db_column_name = d.pop("dbColumnName", UNSET)

        _db_column_type = d.pop("dbColumnType", UNSET)
        db_column_type: Union[Unset, PublishSchemaDtoDbColumnType]
        if isinstance(_db_column_type, Unset):
            db_column_type = UNSET
        else:
            db_column_type = PublishSchemaDtoDbColumnType(_db_column_type)

        publish_schema_dto = cls(
            id=id,
            process_scheme=process_scheme,
            sub_process=sub_process,
            process_step=process_step,
            field_name=field_name,
            field_unit=field_unit,
            field_order=field_order,
            field_data_type=field_data_type,
            process_step_type=process_step_type,
            db_column_name=db_column_name,
            db_column_type=db_column_type,
        )

        publish_schema_dto.additional_properties = d
        return publish_schema_dto

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
