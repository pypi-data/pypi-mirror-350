from yield_sdk.api_client import SyncAPIClient
from yield_sdk.api_result import APIResult
from . import order_payloads as payloads


class SyncOrderClient:
    _base: "SyncOrderBaseClient"

    def __init__(self, base_client: "SyncOrderBaseClient"):
        self._base = base_client

    def fetch(self, id: str) -> payloads.Order:
        return self._base.fetch(id).data

    def create(self, params: payloads.OrderCreateParams) -> payloads.Order:
        return self._base.create(params).data


class SyncOrderBaseClient:
    _api: SyncAPIClient

    def __init__(self, api_client: SyncAPIClient):
        self._api = api_client

    def fetch(self, id: str) -> APIResult[payloads.Order]:
        response = self._api.run_query(f"/order/fetch/{id}")

        return SyncAPIClient.process_response(response, payloads.Order.from_payload)

    def create(self, params: payloads.OrderCreateParams) -> APIResult[payloads.Order]:
        payload = payloads.OrderCreatePayload.build(params)
        response = self._api.run_command(f"/order/create", payload)

        return SyncAPIClient.process_response(response, payloads.Order.from_payload)
