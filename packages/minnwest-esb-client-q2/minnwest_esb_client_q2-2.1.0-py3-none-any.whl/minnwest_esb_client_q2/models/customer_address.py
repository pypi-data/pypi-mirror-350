from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomerAddress")


@_attrs_define
class CustomerAddress:
    """
    Attributes:
        inst_number (Union[None, Unset, str]):
        address_id (Union[None, Unset, str]):
        address (Union[None, Unset, str]):
        address2 (Union[None, Unset, str]):
        city_state_zip (Union[None, Unset, str]):
        city (Union[None, Unset, str]):
        state (Union[None, Unset, str]):
        zip_ (Union[None, Unset, str]):
    """

    inst_number: Union[None, Unset, str] = UNSET
    address_id: Union[None, Unset, str] = UNSET
    address: Union[None, Unset, str] = UNSET
    address2: Union[None, Unset, str] = UNSET
    city_state_zip: Union[None, Unset, str] = UNSET
    city: Union[None, Unset, str] = UNSET
    state: Union[None, Unset, str] = UNSET
    zip_: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        inst_number: Union[None, Unset, str]
        if isinstance(self.inst_number, Unset):
            inst_number = UNSET
        else:
            inst_number = self.inst_number

        address_id: Union[None, Unset, str]
        if isinstance(self.address_id, Unset):
            address_id = UNSET
        else:
            address_id = self.address_id

        address: Union[None, Unset, str]
        if isinstance(self.address, Unset):
            address = UNSET
        else:
            address = self.address

        address2: Union[None, Unset, str]
        if isinstance(self.address2, Unset):
            address2 = UNSET
        else:
            address2 = self.address2

        city_state_zip: Union[None, Unset, str]
        if isinstance(self.city_state_zip, Unset):
            city_state_zip = UNSET
        else:
            city_state_zip = self.city_state_zip

        city: Union[None, Unset, str]
        if isinstance(self.city, Unset):
            city = UNSET
        else:
            city = self.city

        state: Union[None, Unset, str]
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        zip_: Union[None, Unset, str]
        if isinstance(self.zip_, Unset):
            zip_ = UNSET
        else:
            zip_ = self.zip_

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if inst_number is not UNSET:
            field_dict["instNumber"] = inst_number
        if address_id is not UNSET:
            field_dict["addressId"] = address_id
        if address is not UNSET:
            field_dict["address"] = address
        if address2 is not UNSET:
            field_dict["address2"] = address2
        if city_state_zip is not UNSET:
            field_dict["cityStateZip"] = city_state_zip
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if zip_ is not UNSET:
            field_dict["zip"] = zip_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_inst_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inst_number = _parse_inst_number(d.pop("instNumber", UNSET))

        def _parse_address_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address_id = _parse_address_id(d.pop("addressId", UNSET))

        def _parse_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address = _parse_address(d.pop("address", UNSET))

        def _parse_address2(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        address2 = _parse_address2(d.pop("address2", UNSET))

        def _parse_city_state_zip(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        city_state_zip = _parse_city_state_zip(d.pop("cityStateZip", UNSET))

        def _parse_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        city = _parse_city(d.pop("city", UNSET))

        def _parse_state(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        state = _parse_state(d.pop("state", UNSET))

        def _parse_zip_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        zip_ = _parse_zip_(d.pop("zip", UNSET))

        customer_address = cls(
            inst_number=inst_number,
            address_id=address_id,
            address=address,
            address2=address2,
            city_state_zip=city_state_zip,
            city=city,
            state=state,
            zip_=zip_,
        )

        return customer_address
