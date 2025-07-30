from . import modules as m
from .api_client import SyncAPIClient


class SyncClient:
    _base: "SyncBaseClient"

    _self: m.self.SyncSelfClient
    _order: m.order.SyncOrderClient

    def __init__(self, api_key: str):
        self._base = SyncBaseClient(api_key)

        self._self = m.self.SyncSelfClient(self._base.self)
        self._order = m.order.SyncOrderClient(self._base.order)

    @property
    def base(self) -> "SyncBaseClient":
        return self._base

    @property
    def self(self) -> m.self.SyncSelfClient:
        return self._self

    @property
    def order(self) -> m.order.SyncOrderClient:
        return self._order

    def close(self) -> None:
        self._base.close()


class SyncBaseClient:
    _api: SyncAPIClient

    _self: m.self.SyncSelfBaseClient
    _order: m.order.SyncOrderBaseClient

    def __init__(self, api_key: str):
        self._api = SyncAPIClient(api_key)

        self._self = m.self.SyncSelfBaseClient(self._api)
        self._order = m.order.SyncOrderBaseClient(self._api)

    @property
    def api(self) -> SyncAPIClient:
        return self._api

    @property
    def self(self) -> m.self.SyncSelfBaseClient:
        return self._self

    @property
    def order(self) -> m.order.SyncOrderBaseClient:
        return self._order

    def close(self) -> None:
        self._api.close()
