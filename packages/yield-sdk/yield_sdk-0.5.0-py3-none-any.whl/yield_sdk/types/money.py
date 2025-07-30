import dataclasses as dc
import decimal
import re

@dc.dataclass(frozen=True, slots=True)
class Money:
    currency_code: str
    value: decimal.Decimal

    @classmethod
    def from_payload(cls, payload: str) -> "Money":
        m = re.match(r"^([A-Z]{3}) (-?\d+(?:\.\d+)?)$", payload)
        if m is None:
            raise ValueError(f"Invalid money: {payload}")

        return cls(m[1], decimal.Decimal(m[2]))
