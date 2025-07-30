from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerPhoneData")


@_attrs_define
class CustomerPhoneData:
    """
    Attributes:
        phone_code (Union[None, Unset, int]):
        phone_code_enum_type (Union[None, Unset, str]):
        phone_intl (Union[None, Unset, int]):
        phone_area (Union[None, Unset, int]):
        phone_number (Union[None, Unset, int]):
        phone_description (Union[None, Unset, str]):
        phone_ext (Union[None, Unset, int]):
    """

    phone_code: Union[None, Unset, int] = UNSET
    phone_code_enum_type: Union[None, Unset, str] = UNSET
    phone_intl: Union[None, Unset, int] = UNSET
    phone_area: Union[None, Unset, int] = UNSET
    phone_number: Union[None, Unset, int] = UNSET
    phone_description: Union[None, Unset, str] = UNSET
    phone_ext: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        phone_code: Union[None, Unset, int]
        if isinstance(self.phone_code, Unset):
            phone_code = UNSET
        else:
            phone_code = self.phone_code

        phone_code_enum_type: Union[None, Unset, str]
        if isinstance(self.phone_code_enum_type, Unset):
            phone_code_enum_type = UNSET
        else:
            phone_code_enum_type = self.phone_code_enum_type

        phone_intl: Union[None, Unset, int]
        if isinstance(self.phone_intl, Unset):
            phone_intl = UNSET
        else:
            phone_intl = self.phone_intl

        phone_area: Union[None, Unset, int]
        if isinstance(self.phone_area, Unset):
            phone_area = UNSET
        else:
            phone_area = self.phone_area

        phone_number: Union[None, Unset, int]
        if isinstance(self.phone_number, Unset):
            phone_number = UNSET
        else:
            phone_number = self.phone_number

        phone_description: Union[None, Unset, str]
        if isinstance(self.phone_description, Unset):
            phone_description = UNSET
        else:
            phone_description = self.phone_description

        phone_ext: Union[None, Unset, int]
        if isinstance(self.phone_ext, Unset):
            phone_ext = UNSET
        else:
            phone_ext = self.phone_ext

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if phone_code is not UNSET:
            field_dict["phoneCode"] = phone_code
        if phone_code_enum_type is not UNSET:
            field_dict["phoneCodeEnumType"] = phone_code_enum_type
        if phone_intl is not UNSET:
            field_dict["phoneIntl"] = phone_intl
        if phone_area is not UNSET:
            field_dict["phoneArea"] = phone_area
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if phone_description is not UNSET:
            field_dict["phoneDescription"] = phone_description
        if phone_ext is not UNSET:
            field_dict["phoneExt"] = phone_ext

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_phone_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        phone_code = _parse_phone_code(d.pop("phoneCode", UNSET))

        def _parse_phone_code_enum_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone_code_enum_type = _parse_phone_code_enum_type(d.pop("phoneCodeEnumType", UNSET))

        def _parse_phone_intl(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        phone_intl = _parse_phone_intl(d.pop("phoneIntl", UNSET))

        def _parse_phone_area(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        phone_area = _parse_phone_area(d.pop("phoneArea", UNSET))

        def _parse_phone_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        phone_number = _parse_phone_number(d.pop("phoneNumber", UNSET))

        def _parse_phone_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        phone_description = _parse_phone_description(d.pop("phoneDescription", UNSET))

        def _parse_phone_ext(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        phone_ext = _parse_phone_ext(d.pop("phoneExt", UNSET))

        customer_phone_data = cls(
            phone_code=phone_code,
            phone_code_enum_type=phone_code_enum_type,
            phone_intl=phone_intl,
            phone_area=phone_area,
            phone_number=phone_number,
            phone_description=phone_description,
            phone_ext=phone_ext,
        )

        return customer_phone_data
