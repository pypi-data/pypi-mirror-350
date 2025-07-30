from enum import Enum


class AccountType(str, Enum):
    CERTIFICATE = "Certificate"
    CHECKING = "Checking"
    DDALOAN = "DdaLoan"
    LOAN = "Loan"
    SAVINGS = "Savings"
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        return str(self.value)
