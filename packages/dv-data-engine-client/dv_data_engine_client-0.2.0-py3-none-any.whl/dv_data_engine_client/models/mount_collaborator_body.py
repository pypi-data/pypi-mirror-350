from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mount_collaborator_body_columns_item import MountCollaboratorBodyColumnsItem


T = TypeVar("T", bound="MountCollaboratorBody")


@_attrs_define
class MountCollaboratorBody:
    """
    Attributes:
        columns (Union[Unset, list['MountCollaboratorBodyColumnsItem']]): The columns to create for a data consumer.
            This is ignored for data providers.
    """

    columns: Union[Unset, list["MountCollaboratorBodyColumnsItem"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        columns: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if columns is not UNSET:
            field_dict["columns"] = columns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mount_collaborator_body_columns_item import MountCollaboratorBodyColumnsItem

        d = dict(src_dict)
        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = MountCollaboratorBodyColumnsItem.from_dict(columns_item_data)

            columns.append(columns_item)

        mount_collaborator_body = cls(
            columns=columns,
        )

        mount_collaborator_body.additional_properties = d
        return mount_collaborator_body

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
