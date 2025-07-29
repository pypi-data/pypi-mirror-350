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


class TradeClient:
    """
    A client for interacting with the Crypticorn Trade API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
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
