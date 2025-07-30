from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerContactData")


@_attrs_define
class CustomerContactData:
    """
    Attributes:
        contact_code (Union[None, Unset, int]):
        contact_code_enum_type (Union[None, Unset, str]):
        contact_info (Union[None, Unset, str]):
    """

    contact_code: Union[None, Unset, int] = UNSET
    contact_code_enum_type: Union[None, Unset, str] = UNSET
    contact_info: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        contact_code: Union[None, Unset, int]
        if isinstance(self.contact_code, Unset):
            contact_code = UNSET
        else:
            contact_code = self.contact_code

        contact_code_enum_type: Union[None, Unset, str]
        if isinstance(self.contact_code_enum_type, Unset):
            contact_code_enum_type = UNSET
        else:
            contact_code_enum_type = self.contact_code_enum_type

        contact_info: Union[None, Unset, str]
        if isinstance(self.contact_info, Unset):
            contact_info = UNSET
        else:
            contact_info = self.contact_info

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if contact_code is not UNSET:
            field_dict["contactCode"] = contact_code
        if contact_code_enum_type is not UNSET:
            field_dict["contactCodeEnumType"] = contact_code_enum_type
        if contact_info is not UNSET:
            field_dict["contactInfo"] = contact_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_contact_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        contact_code = _parse_contact_code(d.pop("contactCode", UNSET))

        def _parse_contact_code_enum_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        contact_code_enum_type = _parse_contact_code_enum_type(d.pop("contactCodeEnumType", UNSET))

        def _parse_contact_info(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        contact_info = _parse_contact_info(d.pop("contactInfo", UNSET))

        customer_contact_data = cls(
            contact_code=contact_code,
            contact_code_enum_type=contact_code_enum_type,
            contact_info=contact_info,
        )

        return customer_contact_data
