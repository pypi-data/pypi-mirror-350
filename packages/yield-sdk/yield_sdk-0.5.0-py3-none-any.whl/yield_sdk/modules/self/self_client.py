from yield_sdk.api_client import SyncAPIClient
from yield_sdk.api_result import APIResult
from . import self_payloads as payloads


class SyncSelfClient:
    _base: "SyncSelfBaseClient"

    def __init__(self, base_client: "SyncSelfBaseClient"):
        self._base = base_client

    def info(self) -> payloads.SelfInfo:
        return self._base.info().data


class SyncSelfBaseClient:
    _api: SyncAPIClient

    def __init__(self, api_client: SyncAPIClient):
        self._api = api_client

    def info(self) -> APIResult[payloads.SelfInfo]:
        response = self._api.run_query("/self/info")

        return SyncAPIClient.process_response(response, payloads.SelfInfo.from_payload)
