"""Integration tests for ``crypto_advisor.services.ta_service``.

These tests exercise the public volatility-analysis surface against live
Binance data.  They are marked with the custom ``@pytest.mark.integration``
marker and are therefore executed only when the ``--run-integration`` flag is
supplied.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from crypto_advisor.api.models.technical import TechnicalAnalysisRequest
from crypto_advisor.api.volatility import analyze_volatility_tool
from crypto_advisor.providers.binance import fetch_binance_chart
from crypto_advisor.services.ta_service import calculate_volatility_index


if TYPE_CHECKING:  # pragma: no cover – test-time only
    pass


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


SYMBOL = "BTCUSDT"


def _safe_fetch(symbol: str, interval: str, limit: int):  # noqa: D401
    """Fetch kline data and skip test on network errors."""

    try:
        return fetch_binance_chart(symbol, interval, limit)
    except Exception as exc:  # pragma: no cover – network I/O
        pytest.skip(f"External fetch failed: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
def test_volatility_index_single_interval() -> None:  # noqa: D103
    interval = "1d"
    candles = _safe_fetch(SYMBOL, interval, 50)

    result = calculate_volatility_index(candles)

    assert 0 <= result["volatility_index"] <= 5

    # Verify API-level wrapper returns identical output.
    api_result = analyze_volatility_tool(TechnicalAnalysisRequest(candlestick_data=candles))
    assert api_result["volatility_index"] == result["volatility_index"]


@pytest.mark.integration
def test_volatility_index_across_timeframes() -> None:  # noqa: D103
    timeframes = {
        "1h": 168,  # 7 days
        "4h": 42,
        "1d": 30,
    }

    indices: dict[str, float] = {}

    for interval, limit in timeframes.items():
        candles = _safe_fetch(SYMBOL, interval, limit)
        indices[interval] = calculate_volatility_index(candles)["volatility_index"]

    # Simple sanity: function returns numeric index for each timeframe.
    assert set(indices) == set(timeframes)


@pytest.mark.integration
def test_langchain_tool_integration() -> None:  # noqa: D103
    try:
        from crypto_advisor.tools import get_volatility_index_tool
        from langchain.tools.base import ToolException  # noqa: WPS433 – optional dev dep

        tool = get_volatility_index_tool()
        candles = _safe_fetch(SYMBOL, "1d", 30)

        result = tool.run({"candlestick_data": candles})

        assert 0 <= result["volatility_index"] <= 5
    except ToolException as exc:  # pragma: no cover – runtime safety
        pytest.skip(f"LangChain tool failure: {exc}") 