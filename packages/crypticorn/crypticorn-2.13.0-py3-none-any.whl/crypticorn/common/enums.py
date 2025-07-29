"""Defines common enumerations used throughout the codebase for type safety and consistency."""

try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum

from crypticorn.common.mixins import ValidateEnumMixin


class Exchange(ValidateEnumMixin, StrEnum):
    """Supported exchanges for trading"""

    KUCOIN = "kucoin"
    BINGX = "bingx"
    HYPERLIQUID = "hyperliquid"


class InternalExchange(ValidateEnumMixin, StrEnum):
    """All exchanges we are using, including public (Exchange)"""

    KUCOIN = "kucoin"
    BINGX = "bingx"
    BINANCE = "binance"
    BYBIT = "bybit"
    HYPERLIQUID = "hyperliquid"
    BITGET = "bitget"


class MarketType(ValidateEnumMixin, StrEnum):
    """
    Market types
    """

    SPOT = "spot"
    FUTURES = "futures"
