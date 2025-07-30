from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.job_dto_status import JobDtoStatus
from ..models.job_dto_type import JobDtoType
from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.job_process_basic_report_result import JobProcessBasicReportResult
    from ..models.job_process_downsampling_result import JobProcessDownsamplingResult
    from ..models.job_process_export_result import JobProcessExportResult
    from ..models.job_process_import_result import JobProcessImportResult
    from ..models.job_process_offline_import_result import JobProcessOfflineImportResult
    from ..models.job_sampling_offline_data_import_result import JobSamplingOfflineDataImportResult
    from ..models.job_sampling_offline_import_auto_result import JobSamplingOfflineImportAutoResult
    from ..models.job_sampling_rescan_result import JobSamplingRescanResult
    from ..models.user_editor_dto import UserEditorDto


T = TypeVar("T", bound="JobDto")


@_attrs_define
class JobDto:
    """
    Attributes:
        id (Union[Unset, int]):
        name (Union[Unset, str]):
        start_date (Union[Unset, int]):
        end_date (Union[Unset, int]):
        status (Union[Unset, JobDtoStatus]):
        type (Union[Unset, JobDtoType]):
        user (Union[Unset, UserEditorDto]):
        progress_ready_units (Union[Unset, int]):
        progress_total_units (Union[Unset, int]):
        error_message (Union[Unset, str]):
        has_artifact (Union[Unset, bool]):
        result (Union['JobProcessBasicReportResult', 'JobProcessDownsamplingResult', 'JobProcessExportResult',
            'JobProcessImportResult', 'JobProcessOfflineImportResult', 'JobSamplingOfflineDataImportResult',
            'JobSamplingOfflineImportAutoResult', 'JobSamplingRescanResult', Unset]):
    """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    start_date: Union[Unset, int] = UNSET
    end_date: Union[Unset, int] = UNSET
    status: Union[Unset, JobDtoStatus] = UNSET
    type: Union[Unset, JobDtoType] = UNSET
    user: Union[Unset, "UserEditorDto"] = UNSET
    progress_ready_units: Union[Unset, int] = UNSET
    progress_total_units: Union[Unset, int] = UNSET
    error_message: Union[Unset, str] = UNSET
    has_artifact: Union[Unset, bool] = UNSET
    result: Union[
        "JobProcessBasicReportResult",
        "JobProcessDownsamplingResult",
        "JobProcessExportResult",
        "JobProcessImportResult",
        "JobProcessOfflineImportResult",
        "JobSamplingOfflineDataImportResult",
        "JobSamplingOfflineImportAutoResult",
        "JobSamplingRescanResult",
        Unset,
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.job_process_basic_report_result import JobProcessBasicReportResult
        from ..models.job_process_downsampling_result import JobProcessDownsamplingResult
        from ..models.job_process_export_result import JobProcessExportResult
        from ..models.job_process_import_result import JobProcessImportResult
        from ..models.job_process_offline_import_result import JobProcessOfflineImportResult
        from ..models.job_sampling_offline_data_import_result import JobSamplingOfflineDataImportResult
        from ..models.job_sampling_offline_import_auto_result import JobSamplingOfflineImportAutoResult

        id = self.id

        name = self.name

        start_date = self.start_date

        end_date = self.end_date

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        user: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        progress_ready_units = self.progress_ready_units

        progress_total_units = self.progress_total_units

        error_message = self.error_message

        has_artifact = self.has_artifact

        result: Union[Dict[str, Any], Unset]
        if isinstance(self.result, Unset):
            result = UNSET
        elif isinstance(self.result, JobProcessBasicReportResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobProcessDownsamplingResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobProcessExportResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobProcessImportResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobProcessOfflineImportResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobSamplingOfflineDataImportResult):
            result = self.result.to_dict()
        elif isinstance(self.result, JobSamplingOfflineImportAutoResult):
            result = self.result.to_dict()
        else:
            result = self.result.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if end_date is not UNSET:
            field_dict["endDate"] = end_date
        if status is not UNSET:
            field_dict["status"] = status
        if type is not UNSET:
            field_dict["type"] = type
        if user is not UNSET:
            field_dict["user"] = user
        if progress_ready_units is not UNSET:
            field_dict["progressReadyUnits"] = progress_ready_units
        if progress_total_units is not UNSET:
            field_dict["progressTotalUnits"] = progress_total_units
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if has_artifact is not UNSET:
            field_dict["hasArtifact"] = has_artifact
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.job_process_basic_report_result import JobProcessBasicReportResult
        from ..models.job_process_downsampling_result import JobProcessDownsamplingResult
        from ..models.job_process_export_result import JobProcessExportResult
        from ..models.job_process_import_result import JobProcessImportResult
        from ..models.job_process_offline_import_result import JobProcessOfflineImportResult
        from ..models.job_sampling_offline_data_import_result import JobSamplingOfflineDataImportResult
        from ..models.job_sampling_offline_import_auto_result import JobSamplingOfflineImportAutoResult
        from ..models.job_sampling_rescan_result import JobSamplingRescanResult
        from ..models.user_editor_dto import UserEditorDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        start_date = d.pop("startDate", UNSET)

        end_date = d.pop("endDate", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, JobDtoStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = JobDtoStatus(_status)

        _type = d.pop("type", UNSET)
        type: Union[Unset, JobDtoType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = JobDtoType(_type)

        _user = d.pop("user", UNSET)
        user: Union[Unset, UserEditorDto]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = UserEditorDto.from_dict(_user)

        progress_ready_units = d.pop("progressReadyUnits", UNSET)

        progress_total_units = d.pop("progressTotalUnits", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        has_artifact = d.pop("hasArtifact", UNSET)

        def _parse_result(
            data: object,
        ) -> Union[
            "JobProcessBasicReportResult",
            "JobProcessDownsamplingResult",
            "JobProcessExportResult",
            "JobProcessImportResult",
            "JobProcessOfflineImportResult",
            "JobSamplingOfflineDataImportResult",
            "JobSamplingOfflineImportAutoResult",
            "JobSamplingRescanResult",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_0 = JobProcessBasicReportResult.from_dict(data)

                return result_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_1 = JobProcessDownsamplingResult.from_dict(data)

                return result_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_2 = JobProcessExportResult.from_dict(data)

                return result_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_3 = JobProcessImportResult.from_dict(data)

                return result_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_4 = JobProcessOfflineImportResult.from_dict(data)

                return result_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_5 = JobSamplingOfflineDataImportResult.from_dict(data)

                return result_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                result_type_6 = JobSamplingOfflineImportAutoResult.from_dict(data)

                return result_type_6
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            result_type_7 = JobSamplingRescanResult.from_dict(data)

            return result_type_7

        result = _parse_result(d.pop("result", UNSET))

        job_dto = cls(
            id=id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            status=status,
            type=type,
            user=user,
            progress_ready_units=progress_ready_units,
            progress_total_units=progress_total_units,
            error_message=error_message,
            has_artifact=has_artifact,
            result=result,
        )

        job_dto.additional_properties = d
        return job_dto

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
