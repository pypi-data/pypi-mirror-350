from __future__ import annotations
from crypticorn.metrics import (
    ApiClient,
    Configuration,
    ExchangesApi,
    StatusApi,
    IndicatorsApi,
    LogsApi,
    MarketcapApi,
    MarketsApi,
    TokensApi,
    AdminApi,
    QuoteCurrenciesApi,
)
from crypticorn.common import optional_import


class MetricsClient:
    """
    A client for interacting with the Crypticorn Metrics API.
    """

    config_class = Configuration

    def __init__(
        self,
        config: Configuration,
    ):
        self.config = config
        self.base_client = ApiClient(configuration=self.config)
        # Instantiate all the endpoint clients
        self.status = StatusApi(self.base_client)
        self.indicators = IndicatorsApi(self.base_client)
        self.logs = LogsApi(self.base_client)
        self.marketcap = MarketcapApiWrapper(self.base_client)
        self.markets = MarketsApi(self.base_client)
        self.tokens = TokensApiWrapper(self.base_client)
        self.exchanges = ExchangesApiWrapper(self.base_client)
        self.quote_currencies = QuoteCurrenciesApi(self.base_client)
        self.admin = AdminApi(self.base_client)


class MarketcapApiWrapper(MarketcapApi):
    """
    A wrapper for the MarketcapApi class.
    """

    async def get_marketcap_symbols_fmt(self, *args, **kwargs) -> pd.DataFrame:  # type: ignore
        """
        Get the marketcap symbols in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_marketcap_symbols(*args, **kwargs)
        rows = []
        for item in response:
            row = {"timestamp": item.timestamp}
            row.update({i + 1: sym for i, sym in enumerate(item.symbols)})
            rows.append(row)
        df = pd.DataFrame(rows)
        return df


class TokensApiWrapper(TokensApi):
    """
    A wrapper for the TokensApi class.
    """

    async def get_stable_tokens_fmt(self, *args, **kwargs) -> pd.DataFrame:  # type: ignore
        """
        Get the tokens in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_stable_tokens(*args, **kwargs)
        return pd.DataFrame(response)

    async def get_wrapped_tokens_fmt(self, *args, **kwargs) -> pd.DataFrame:  # type: ignore
        """
        Get the wrapped tokens in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_wrapped_tokens(*args, **kwargs)
        return pd.DataFrame(response)


class ExchangesApiWrapper(ExchangesApi):
    """
    A wrapper for the ExchangesApi class.
    """

    async def get_available_exchanges_fmt(self, *args, **kwargs) -> pd.DataFrame:  # type: ignore
        """
        Get the exchanges in a pandas dataframe
        """
        pd = optional_import("pandas", "extra")
        response = await self.get_available_exchanges(*args, **kwargs)

        # Create list of dictionaries with timestamp and flattened exchange data
        rows = []
        for item in response:
            row = {"timestamp": item.timestamp}
            row.update(
                item.exchanges
            )  # This spreads the exchanges dict into individual columns
            rows.append(row)

        df = pd.DataFrame(rows)
        return df
