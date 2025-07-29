from crypticorn.pay import (
    ApiClient,
    Configuration,
    NOWPaymentsApi,
    StatusApi,
    PaymentsApi,
    ProductsApi,
    AdminApi,
)


class PayClient:
    """
    A client for interacting with the Crypticorn Pay API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        self.now = NOWPaymentsApi(self.base_client)
        self.status = StatusApi(self.base_client)
        self.payments = PaymentsApi(self.base_client)
        self.products = ProductsApi(self.base_client)
        self.admin = AdminApi(self.base_client)
