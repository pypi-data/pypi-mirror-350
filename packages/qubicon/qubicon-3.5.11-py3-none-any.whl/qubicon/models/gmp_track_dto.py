from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from qubicon.api.types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gmp_track_confirmation_dto import GmpTrackConfirmationDto


T = TypeVar("T", bound="GmpTrackDto")


@_attrs_define
class GmpTrackDto:
    """
    Attributes:
        id (Union[Unset, int]):
        finalized (Union[Unset, bool]):
        async_ (Union[Unset, bool]):
        cancelled (Union[Unset, bool]):
        confirmations (Union[Unset, List['GmpTrackConfirmationDto']]):
    """

    id: Union[Unset, int] = UNSET
    finalized: Union[Unset, bool] = UNSET
    async_: Union[Unset, bool] = UNSET
    cancelled: Union[Unset, bool] = UNSET
    confirmations: Union[Unset, List["GmpTrackConfirmationDto"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        finalized = self.finalized

        async_ = self.async_

        cancelled = self.cancelled

        confirmations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.confirmations, Unset):
            confirmations = []
            for confirmations_item_data in self.confirmations:
                confirmations_item = confirmations_item_data.to_dict()
                confirmations.append(confirmations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if finalized is not UNSET:
            field_dict["finalized"] = finalized
        if async_ is not UNSET:
            field_dict["async"] = async_
        if cancelled is not UNSET:
            field_dict["cancelled"] = cancelled
        if confirmations is not UNSET:
            field_dict["confirmations"] = confirmations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.gmp_track_confirmation_dto import GmpTrackConfirmationDto

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        finalized = d.pop("finalized", UNSET)

        async_ = d.pop("async", UNSET)

        cancelled = d.pop("cancelled", UNSET)

        confirmations = []
        _confirmations = d.pop("confirmations", UNSET)
        for confirmations_item_data in _confirmations or []:
            confirmations_item = GmpTrackConfirmationDto.from_dict(confirmations_item_data)

            confirmations.append(confirmations_item)

        gmp_track_dto = cls(
            id=id,
            finalized=finalized,
            async_=async_,
            cancelled=cancelled,
            confirmations=confirmations,
        )

        gmp_track_dto.additional_properties = d
        return gmp_track_dto

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
