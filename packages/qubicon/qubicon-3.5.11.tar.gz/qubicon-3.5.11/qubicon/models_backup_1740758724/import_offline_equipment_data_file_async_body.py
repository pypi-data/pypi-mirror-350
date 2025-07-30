from io import BytesIO
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import File

T = TypeVar("T", bound="ImportOfflineEquipmentDataFileAsyncBody")


@_attrs_define
class ImportOfflineEquipmentDataFileAsyncBody:
    """
    Attributes:
        import_file (File):
    """

    import_file: File
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        import_file = self.import_file.to_tuple()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "importFile": import_file,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        import_file = self.import_file.to_tuple()

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "importFile": import_file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        import_file = File(payload=BytesIO(d.pop("importFile")))

        import_offline_equipment_data_file_async_body = cls(
            import_file=import_file,
        )

        import_offline_equipment_data_file_async_body.additional_properties = d
        return import_offline_equipment_data_file_async_body

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
