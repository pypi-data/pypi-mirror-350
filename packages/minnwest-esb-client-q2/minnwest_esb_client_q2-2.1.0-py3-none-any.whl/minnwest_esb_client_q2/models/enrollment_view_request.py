from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="EnrollmentViewRequest")


@_attrs_define
class EnrollmentViewRequest:
    """
    Attributes:
        portfolio (str):
    """

    portfolio: str

    def to_dict(self) -> dict[str, Any]:
        portfolio = self.portfolio

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "portfolio": portfolio,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        portfolio = d.pop("portfolio")

        enrollment_view_request = cls(
            portfolio=portfolio,
        )

        return enrollment_view_request
