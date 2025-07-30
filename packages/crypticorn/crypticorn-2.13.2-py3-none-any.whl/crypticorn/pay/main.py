from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from crypticorn.pay import (
    ApiClient,
    Configuration,
    NOWPaymentsApi,
    StatusApi,
    PaymentsApi,
    ProductsApi,
    AdminApi,
)

if TYPE_CHECKING:
    from aiohttp import ClientSession


class PayClient:
    """
    A client for interacting with the Crypticorn Pay API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
        http_client: Optional[ClientSession] = None,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        self.base_client.rest_client.pool_manager = http_client
        self.now = NOWPaymentsApi(self.base_client)
        self.status = StatusApi(self.base_client)
        self.payments = PaymentsApi(self.base_client)
        self.products = ProductsApi(self.base_client)
        self.admin = AdminApi(self.base_client)
