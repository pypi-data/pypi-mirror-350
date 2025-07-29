from crypticorn.auth import (
    ApiClient,
    Configuration,
    AdminApi,
    ServiceApi,
    UserApi,
    WalletApi,
    AuthApi,
)


class AuthClient:
    """
    A client for interacting with the Crypticorn Auth API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.admin = AdminApi(self.base_client)
        self.service = ServiceApi(self.base_client)
        self.user = UserApi(self.base_client)
        self.wallet = WalletApi(self.base_client)
        self.login = AuthApi(self.base_client)
