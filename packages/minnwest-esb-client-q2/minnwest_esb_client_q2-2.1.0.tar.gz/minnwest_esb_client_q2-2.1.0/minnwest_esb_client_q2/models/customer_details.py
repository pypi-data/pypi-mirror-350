from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer_address import CustomerAddress
    from ..models.customer_contact_data import CustomerContactData
    from ..models.customer_phone_data import CustomerPhoneData


T = TypeVar("T", bound="CustomerDetails")


@_attrs_define
class CustomerDetails:
    """
    Attributes:
        inst_number (Union[Unset, int]):
        name_id (Union[None, Unset, str]):
        customer_type (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        short_last_name (Union[None, Unset, str]):
        short_first_name (Union[None, Unset, str]):
        middle_initial (Union[None, Unset, str]):
        tax_id_code (Union[None, Unset, str]):
        tax_id_number (Union[None, Unset, int]):
        tax_id_enum_type (Union[None, Unset, str]):
        tax_id_type (Union[None, Unset, str]):
        customer_phone_data_list (Union[None, Unset, list['CustomerPhoneData']]):
        customer_contact_data_list (Union[None, Unset, list['CustomerContactData']]):
        customer_address_list (Union[None, Unset, list['CustomerAddress']]):
    """

    inst_number: Union[Unset, int] = UNSET
    name_id: Union[None, Unset, str] = UNSET
    customer_type: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    short_last_name: Union[None, Unset, str] = UNSET
    short_first_name: Union[None, Unset, str] = UNSET
    middle_initial: Union[None, Unset, str] = UNSET
    tax_id_code: Union[None, Unset, str] = UNSET
    tax_id_number: Union[None, Unset, int] = UNSET
    tax_id_enum_type: Union[None, Unset, str] = UNSET
    tax_id_type: Union[None, Unset, str] = UNSET
    customer_phone_data_list: Union[None, Unset, list["CustomerPhoneData"]] = UNSET
    customer_contact_data_list: Union[None, Unset, list["CustomerContactData"]] = UNSET
    customer_address_list: Union[None, Unset, list["CustomerAddress"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        inst_number = self.inst_number

        name_id: Union[None, Unset, str]
        if isinstance(self.name_id, Unset):
            name_id = UNSET
        else:
            name_id = self.name_id

        customer_type: Union[None, Unset, str]
        if isinstance(self.customer_type, Unset):
            customer_type = UNSET
        else:
            customer_type = self.customer_type

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        short_last_name: Union[None, Unset, str]
        if isinstance(self.short_last_name, Unset):
            short_last_name = UNSET
        else:
            short_last_name = self.short_last_name

        short_first_name: Union[None, Unset, str]
        if isinstance(self.short_first_name, Unset):
            short_first_name = UNSET
        else:
            short_first_name = self.short_first_name

        middle_initial: Union[None, Unset, str]
        if isinstance(self.middle_initial, Unset):
            middle_initial = UNSET
        else:
            middle_initial = self.middle_initial

        tax_id_code: Union[None, Unset, str]
        if isinstance(self.tax_id_code, Unset):
            tax_id_code = UNSET
        else:
            tax_id_code = self.tax_id_code

        tax_id_number: Union[None, Unset, int]
        if isinstance(self.tax_id_number, Unset):
            tax_id_number = UNSET
        else:
            tax_id_number = self.tax_id_number

        tax_id_enum_type: Union[None, Unset, str]
        if isinstance(self.tax_id_enum_type, Unset):
            tax_id_enum_type = UNSET
        else:
            tax_id_enum_type = self.tax_id_enum_type

        tax_id_type: Union[None, Unset, str]
        if isinstance(self.tax_id_type, Unset):
            tax_id_type = UNSET
        else:
            tax_id_type = self.tax_id_type

        customer_phone_data_list: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.customer_phone_data_list, Unset):
            customer_phone_data_list = UNSET
        elif isinstance(self.customer_phone_data_list, list):
            customer_phone_data_list = []
            for customer_phone_data_list_type_0_item_data in self.customer_phone_data_list:
                customer_phone_data_list_type_0_item = customer_phone_data_list_type_0_item_data.to_dict()
                customer_phone_data_list.append(customer_phone_data_list_type_0_item)

        else:
            customer_phone_data_list = self.customer_phone_data_list

        customer_contact_data_list: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.customer_contact_data_list, Unset):
            customer_contact_data_list = UNSET
        elif isinstance(self.customer_contact_data_list, list):
            customer_contact_data_list = []
            for customer_contact_data_list_type_0_item_data in self.customer_contact_data_list:
                customer_contact_data_list_type_0_item = customer_contact_data_list_type_0_item_data.to_dict()
                customer_contact_data_list.append(customer_contact_data_list_type_0_item)

        else:
            customer_contact_data_list = self.customer_contact_data_list

        customer_address_list: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.customer_address_list, Unset):
            customer_address_list = UNSET
        elif isinstance(self.customer_address_list, list):
            customer_address_list = []
            for customer_address_list_type_0_item_data in self.customer_address_list:
                customer_address_list_type_0_item = customer_address_list_type_0_item_data.to_dict()
                customer_address_list.append(customer_address_list_type_0_item)

        else:
            customer_address_list = self.customer_address_list

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if inst_number is not UNSET:
            field_dict["instNumber"] = inst_number
        if name_id is not UNSET:
            field_dict["nameId"] = name_id
        if customer_type is not UNSET:
            field_dict["customerType"] = customer_type
        if name is not UNSET:
            field_dict["name"] = name
        if short_last_name is not UNSET:
            field_dict["shortLastName"] = short_last_name
        if short_first_name is not UNSET:
            field_dict["shortFirstName"] = short_first_name
        if middle_initial is not UNSET:
            field_dict["middleInitial"] = middle_initial
        if tax_id_code is not UNSET:
            field_dict["taxIdCode"] = tax_id_code
        if tax_id_number is not UNSET:
            field_dict["taxIdNumber"] = tax_id_number
        if tax_id_enum_type is not UNSET:
            field_dict["taxIdEnumType"] = tax_id_enum_type
        if tax_id_type is not UNSET:
            field_dict["taxIdType"] = tax_id_type
        if customer_phone_data_list is not UNSET:
            field_dict["customerPhoneDataList"] = customer_phone_data_list
        if customer_contact_data_list is not UNSET:
            field_dict["customerContactDataList"] = customer_contact_data_list
        if customer_address_list is not UNSET:
            field_dict["customerAddressList"] = customer_address_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_address import CustomerAddress
        from ..models.customer_contact_data import CustomerContactData
        from ..models.customer_phone_data import CustomerPhoneData

        d = dict(src_dict)
        inst_number = d.pop("instNumber", UNSET)

        def _parse_name_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name_id = _parse_name_id(d.pop("nameId", UNSET))

        def _parse_customer_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_type = _parse_customer_type(d.pop("customerType", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_short_last_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        short_last_name = _parse_short_last_name(d.pop("shortLastName", UNSET))

        def _parse_short_first_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        short_first_name = _parse_short_first_name(d.pop("shortFirstName", UNSET))

        def _parse_middle_initial(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        middle_initial = _parse_middle_initial(d.pop("middleInitial", UNSET))

        def _parse_tax_id_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tax_id_code = _parse_tax_id_code(d.pop("taxIdCode", UNSET))

        def _parse_tax_id_number(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        tax_id_number = _parse_tax_id_number(d.pop("taxIdNumber", UNSET))

        def _parse_tax_id_enum_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tax_id_enum_type = _parse_tax_id_enum_type(d.pop("taxIdEnumType", UNSET))

        def _parse_tax_id_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tax_id_type = _parse_tax_id_type(d.pop("taxIdType", UNSET))

        def _parse_customer_phone_data_list(data: object) -> Union[None, Unset, list["CustomerPhoneData"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                customer_phone_data_list_type_0 = []
                _customer_phone_data_list_type_0 = data
                for customer_phone_data_list_type_0_item_data in _customer_phone_data_list_type_0:
                    customer_phone_data_list_type_0_item = CustomerPhoneData.from_dict(
                        customer_phone_data_list_type_0_item_data
                    )

                    customer_phone_data_list_type_0.append(customer_phone_data_list_type_0_item)

                return customer_phone_data_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomerPhoneData"]], data)

        customer_phone_data_list = _parse_customer_phone_data_list(d.pop("customerPhoneDataList", UNSET))

        def _parse_customer_contact_data_list(data: object) -> Union[None, Unset, list["CustomerContactData"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                customer_contact_data_list_type_0 = []
                _customer_contact_data_list_type_0 = data
                for customer_contact_data_list_type_0_item_data in _customer_contact_data_list_type_0:
                    customer_contact_data_list_type_0_item = CustomerContactData.from_dict(
                        customer_contact_data_list_type_0_item_data
                    )

                    customer_contact_data_list_type_0.append(customer_contact_data_list_type_0_item)

                return customer_contact_data_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomerContactData"]], data)

        customer_contact_data_list = _parse_customer_contact_data_list(d.pop("customerContactDataList", UNSET))

        def _parse_customer_address_list(data: object) -> Union[None, Unset, list["CustomerAddress"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                customer_address_list_type_0 = []
                _customer_address_list_type_0 = data
                for customer_address_list_type_0_item_data in _customer_address_list_type_0:
                    customer_address_list_type_0_item = CustomerAddress.from_dict(
                        customer_address_list_type_0_item_data
                    )

                    customer_address_list_type_0.append(customer_address_list_type_0_item)

                return customer_address_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomerAddress"]], data)

        customer_address_list = _parse_customer_address_list(d.pop("customerAddressList", UNSET))

        customer_details = cls(
            inst_number=inst_number,
            name_id=name_id,
            customer_type=customer_type,
            name=name,
            short_last_name=short_last_name,
            short_first_name=short_first_name,
            middle_initial=middle_initial,
            tax_id_code=tax_id_code,
            tax_id_number=tax_id_number,
            tax_id_enum_type=tax_id_enum_type,
            tax_id_type=tax_id_type,
            customer_phone_data_list=customer_phone_data_list,
            customer_contact_data_list=customer_contact_data_list,
            customer_address_list=customer_address_list,
        )

        return customer_details
