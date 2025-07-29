from typing import TypedDict


class IBANOplataCreateInvoiceDict(TypedDict):
    organization_name: str
    identification_code: str
    iban: str
    amount: float
    payment_purpose: str
