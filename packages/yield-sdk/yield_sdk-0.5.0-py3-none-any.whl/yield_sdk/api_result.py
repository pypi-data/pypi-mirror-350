from collections.abc import Mapping
import dataclasses as dc
import json
import typing as t


T = t.TypeVar("T")


class APIResult(t.Generic[T]):
    _status_code: int
    _request_id: str | None
    _data: T | None
    _error: "APIErrorDetails | None"

    def __init__(self, status_code: int, request_id: str | None, data: T | None, error: "APIErrorDetails | None"):
        self._status_code = status_code
        self._request_id = request_id
        self._data = data
        self._error = error

    @classmethod
    def success(cls, status_code: int, request_id: str | None, data: T) -> "APIResult[T]":
        return cls(status_code, request_id, data, None)

    @classmethod
    def failure(cls, status_code: int, request_id: str | None, error_type: str, error_body: Mapping[str, object] | None) -> "APIResult[t.Any]":
        return cls(status_code, request_id, None, APIErrorDetails(error_type, error_body))

    @property
    def ok(self) -> bool:
        return self._error is None

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def request_id(self) -> str | None:
        return self._request_id

    @property
    def data(self) -> T:
        if self._data is None:
            raise APIError(self._status_code, self._request_id, self._error) # type: ignore

        return self._data

    @property
    def error(self) -> "APIErrorDetails | None":
        return self._error


@dc.dataclass(frozen=True, slots=True)
class APIErrorDetails:
    type: str
    body: Mapping[str, object] | None


class APIError(Exception):
    _status_code: int
    _request_id: str | None
    _details: APIErrorDetails

    def __init__(self, status_code: int, request_id: str | None, error: APIErrorDetails):
        self._status_code = status_code
        self._request_id = request_id
        self._details = error

        error_info = error.type
        if error_info == "validation_error" and error.body is not None:
            issues = json.dumps(error.body["issues"], ensure_ascii=False, separators=(",", ":"))
            error_info = f"{error_info} {issues}"

        extra_info = "; ".join(f"{k}={v}" for k, v in [
            ("status_code", str(status_code)),
            ("request_id", request_id or "<none>"),
        ])

        super().__init__(f"Yield API error: {error_info} [{extra_info}]")

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def request_id(self) -> str | None:
        return self._request_id

    @property
    def details(self) -> APIErrorDetails:
        return self._details
