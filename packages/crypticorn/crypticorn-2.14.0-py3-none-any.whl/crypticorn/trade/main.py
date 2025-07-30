from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from crypticorn.trade import (
    ApiClient,
    APIKeysApi,
    BotsApi,
    Configuration,
    ExchangesApi,
    FuturesTradingPanelApi,
    NotificationsApi,
    OrdersApi,
    StatusApi,
    StrategiesApi,
    TradingActionsApi,
)

if TYPE_CHECKING:
    from aiohttp import ClientSession


class TradeClient:
    """
    A client for interacting with the Crypticorn Trade API.
    """

    config_class = Configuration

    def __init__(
        self, config: Configuration, http_client: Optional[ClientSession] = None
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        if http_client is not None:
            self.base_client.rest_client.pool_manager = http_client
        # Instantiate all the endpoint clients
        self.bots = BotsApi(self.base_client)
        self.exchanges = ExchangesApi(self.base_client)
        self.notifications = NotificationsApi(self.base_client)
        self.orders = OrdersApi(self.base_client)
        self.status = StatusApi(self.base_client)
        self.strategies = StrategiesApi(self.base_client)
        self.actions = TradingActionsApi(self.base_client)
        self.futures = FuturesTradingPanelApi(self.base_client)
        self.keys = APIKeysApi(self.base_client)
