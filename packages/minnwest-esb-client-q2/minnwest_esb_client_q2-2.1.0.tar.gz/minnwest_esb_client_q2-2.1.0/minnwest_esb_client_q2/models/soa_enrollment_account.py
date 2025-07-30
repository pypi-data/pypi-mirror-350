from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.account_type import AccountType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customer_details import CustomerDetails


T = TypeVar("T", bound="SOAEnrollmentAccount")


@_attrs_define
class SOAEnrollmentAccount:
    """
    Attributes:
        account_number (Union[None, Unset, str]):
        account_type (Union[Unset, AccountType]):
        portfolio (Union[None, Unset, str]):
        customer_details_list (Union[None, Unset, list['CustomerDetails']]):
    """

    account_number: Union[None, Unset, str] = UNSET
    account_type: Union[Unset, AccountType] = UNSET
    portfolio: Union[None, Unset, str] = UNSET
    customer_details_list: Union[None, Unset, list["CustomerDetails"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        account_number: Union[None, Unset, str]
        if isinstance(self.account_number, Unset):
            account_number = UNSET
        else:
            account_number = self.account_number

        account_type: Union[Unset, str] = UNSET
        if not isinstance(self.account_type, Unset):
            account_type = self.account_type.value

        portfolio: Union[None, Unset, str]
        if isinstance(self.portfolio, Unset):
            portfolio = UNSET
        else:
            portfolio = self.portfolio

        customer_details_list: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.customer_details_list, Unset):
            customer_details_list = UNSET
        elif isinstance(self.customer_details_list, list):
            customer_details_list = []
            for customer_details_list_type_0_item_data in self.customer_details_list:
                customer_details_list_type_0_item = customer_details_list_type_0_item_data.to_dict()
                customer_details_list.append(customer_details_list_type_0_item)

        else:
            customer_details_list = self.customer_details_list

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if account_number is not UNSET:
            field_dict["accountNumber"] = account_number
        if account_type is not UNSET:
            field_dict["accountType"] = account_type
        if portfolio is not UNSET:
            field_dict["portfolio"] = portfolio
        if customer_details_list is not UNSET:
            field_dict["customerDetailsList"] = customer_details_list

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customer_details import CustomerDetails

        d = dict(src_dict)

        def _parse_account_number(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        account_number = _parse_account_number(d.pop("accountNumber", UNSET))

        _account_type = d.pop("accountType", UNSET)
        account_type: Union[Unset, AccountType]
        if isinstance(_account_type, Unset):
            account_type = UNSET
        else:
            account_type = AccountType(_account_type)

        def _parse_portfolio(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        portfolio = _parse_portfolio(d.pop("portfolio", UNSET))

        def _parse_customer_details_list(data: object) -> Union[None, Unset, list["CustomerDetails"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                customer_details_list_type_0 = []
                _customer_details_list_type_0 = data
                for customer_details_list_type_0_item_data in _customer_details_list_type_0:
                    customer_details_list_type_0_item = CustomerDetails.from_dict(
                        customer_details_list_type_0_item_data
                    )

                    customer_details_list_type_0.append(customer_details_list_type_0_item)

                return customer_details_list_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomerDetails"]], data)

        customer_details_list = _parse_customer_details_list(d.pop("customerDetailsList", UNSET))

        soa_enrollment_account = cls(
            account_number=account_number,
            account_type=account_type,
            portfolio=portfolio,
            customer_details_list=customer_details_list,
        )

        return soa_enrollment_account
