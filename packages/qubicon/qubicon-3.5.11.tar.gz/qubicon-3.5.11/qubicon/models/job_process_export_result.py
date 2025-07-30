from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.abstract_job_result_job_type import AbstractJobResultJobType

T = TypeVar("T", bound="JobProcessExportResult")


@_attrs_define
class JobProcessExportResult:
    """
    Attributes:
        job_type (AbstractJobResultJobType): Job type
    """

    job_type: AbstractJobResultJobType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_type = self.job_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jobType": job_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_type = AbstractJobResultJobType(d.pop("jobType"))

        job_process_export_result = cls(
            job_type=job_type,
        )

        job_process_export_result.additional_properties = d
        return job_process_export_result

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
