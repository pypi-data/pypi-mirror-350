import dataclasses as dc

from yield_sdk.utils import type_utils


@dc.dataclass(frozen=True, kw_only=True, slots=True)
class SelfInfo:
    id: str
    name: str
    organization: "SelfOrganizationInfo"

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> "SelfInfo":
        return cls(
            id=type_utils.expect_string(payload["id"]),
            name=type_utils.expect_string(payload["name"]),
            organization=SelfOrganizationInfo.from_payload(type_utils.expect_record(payload["organization"])),
        )


@dc.dataclass(frozen=True, kw_only=True, slots=True)
class SelfOrganizationInfo:
    id: str
    registered_name: str
    trade_name: str | None

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> "SelfOrganizationInfo":
        return cls(
            id=type_utils.expect_string(payload["id"]),
            registered_name=type_utils.expect_string(payload["registered_name"]),
            trade_name=type_utils.expect_string(payload["trade_name"]) if payload.get("trade_name") is not None else None,
        )
