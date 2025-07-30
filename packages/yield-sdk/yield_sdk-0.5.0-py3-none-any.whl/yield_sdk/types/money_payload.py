import decimal
import typing as t


# String must be in "{currency_code} {amount}" format (e.g. "PHP 1234.50").
IntoMoneyPayload: t.TypeAlias = "str | tuple[str, decimal.Decimal] | MoneyLike"


class MoneyLike(t.Protocol):
    @property
    def currency_code(self) -> str: ...

    @property
    def value(self) -> decimal.Decimal: ...


class MoneyPayload:
    @classmethod
    def build(cls, money: IntoMoneyPayload) -> str:
        if isinstance(money, str):
            return money
        elif isinstance(money, tuple):
            return f"{money[0]} {money[1]}"
        else:
            return f"{money.currency_code} {money.value}"
