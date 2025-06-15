"""Binance API provider.

This module provides functions for fetching candlestick data from the Binance
REST API using the `requests` library.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final, List, Dict

import requests


API_BASE_URL: Final[str] = "https://api.binance.com/api/v3/klines"


def _parse_candle(raw_candle: list) -> Dict[str, float | datetime]:
    """Convert a single raw kline entry to the internal dict representation.

    The Binance REST API returns each kline (candlestick) as a list with a
    fixed schema.  Only the first six elements are relevant for basic OHLCV
    analysis.

    Args:
        raw_candle: A list obtained from the Binance REST API representing a
            single candlestick.

    Returns:
        A dictionary matching the internal schema expected by downstream
        services.
    """

    open_time: int = raw_candle[0]

    return {
        "time": datetime.fromtimestamp(open_time / 1000),
        "open": float(raw_candle[1]),
        "high": float(raw_candle[2]),
        "low": float(raw_candle[3]),
        "close": float(raw_candle[4]),
        "volume": float(raw_candle[5]),
    }


def fetch_binance_chart(symbol: str, interval: str = "1h", limit: int = 50) -> List[dict]:
    """Fetch candlestick (kline) data from Binance via the public REST API.

    This function avoids heavyweight third-party SDKs and relies on the
    well-documented REST endpoint instead, eliminating indirect dependencies
    (e.g., *websockets*) and potential deprecation warnings.

    Args:
        symbol: Trading pair symbol (e.g. ``"BTCUSDT"``).
        interval: Candlestick interval (e.g. ``"1h"``, ``"4h"``, ``"1d"``).
        limit: Number of candles to retrieve (max 1000 as per Binance API).

    Returns:
        A list of dictionaries containing OHLCV data ordered chronologically.

    Raises:
        RuntimeError: If the REST request fails or returns an error response.
    """

    params: dict[str, str | int] = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
    }

    try:
        response = requests.get(API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover – network I/O
        raise RuntimeError(f"Failed to fetch data from Binance: {exc}") from exc

    raw_data: list[list] = response.json()

    candles = [_parse_candle(candle) for candle in raw_data]

    # Binance returns data in chronological order, matching our expectations.
    return candles

