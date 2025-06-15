"""Unit tests for ``crypto_advisor.services.ta_service``.

These tests validate that each indicator calculation helper adds the expected
columns **and** that the higher-level convenience wrappers return the correct
schema.  The tests rely only on deterministic, in-memory data and therefore run
quickly and without external dependencies.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Dict, List

import pandas as pd
import pytest

from crypto_advisor.services import ta_service

# ---------------------------------------------------------------------------
# Type-only imports to satisfy the workspace's strict type-checking rules.
# ---------------------------------------------------------------------------

if TYPE_CHECKING:  # pragma: no cover – testing utilities only
    pass


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_candlestick_data() -> List[Dict[str, float | str]]:  # noqa: WPS231
    """Create a tiny but realistic OHLCV sample spanning 100 candles.

    A modest amount of volatility is injected every tenth candle to exercise
    the volatility-related indicators without relying on randomness.
    """

    candles: List[Dict[str, float | str]] = []
    base_time = datetime.now(timezone.utc)
    close_price = 1_000.0

    for i in range(100):
        factor = 1.5 if i % 10 == 0 else 1.0

        open_price = close_price
        high_price = open_price * (1 + 0.02 * factor)
        low_price = open_price * (1 - 0.015 * factor)
        close_price = open_price * (1 + 0.003 * (i % 5 - 2) * factor)
        volume = 2_000 * factor

        candles.append(
            {
                "time": (base_time - timedelta(minutes=15 * i)).replace(tzinfo=None).isoformat(),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
            },
        )

    return list(reversed(candles))  # chronological order


# ---------------------------------------------------------------------------
# Column helpers
# ---------------------------------------------------------------------------


TREND_COLS = {"SMA_50", "EMA_20", "ADX"}
MOMENTUM_COLS = {"RSI", "Stoch_RSI_K", "Stoch_RSI_D", "MACD", "MACD_Signal"}
VOLATILITY_COLS = {"Bollinger_High", "Bollinger_Low", "ATR"}
VOLUME_COLS = {"OBV", "CMF", "VWAP"}


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------


def _prepare_df(candles: List[Dict[str, float | str]]) -> pd.DataFrame:
    """Utility: build a typed DataFrame from raw candle dictionaries."""

    df = pd.DataFrame(candles)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df[["open", "high", "low", "close", "volume"]] = df[
        ["open", "high", "low", "close", "volume"]
    ].astype(float)
    return df


@pytest.mark.parametrize(
    "cols, func",
    [
        (TREND_COLS, ta_service.calculate_trend_indicators),
        (MOMENTUM_COLS, ta_service.calculate_momentum_indicators),
        (VOLATILITY_COLS, ta_service.calculate_volatility_indicators),
        (VOLUME_COLS, ta_service.calculate_volume_indicators),
    ],
)
def test_indicator_helpers_add_expected_columns(
    sample_candlestick_data: List[Dict[str, float | str]],
    cols: set[str],
    func,  # type: ignore[no-untyped-def]
) -> None:
    """Each helper should add its expected columns and leave the shape intact."""

    df = _prepare_df(sample_candlestick_data)
    original_len = len(df)

    result = func(df.copy())  # act

    # Same number of rows → no accidental re-indexing
    assert len(result) == original_len

    # Columns present and contain at least one non-null value
    for col in cols:
        assert col in result.columns, f"Missing column: {col}"
        assert result[col].notna().any(), f"All NaNs in column: {col}"


def test_calculate_volatility_index_schema(sample_candlestick_data) -> None:  # noqa: D103
    result = ta_service.calculate_volatility_index(sample_candlestick_data)

    assert set(result) == {
        "volatility_index",
        "volatility_category",
        "components",
        "raw_values",
    }

    # Components and raw values should expose the three sub-keys
    for key in ("atr", "bbw", "hv"):
        assert key in result["raw_values"]

    for key in ("atr_score", "bbw_score", "hv_score"):
        assert key in result["components"]


def test_perform_technical_analysis_returns_latest(sample_candlestick_data) -> None:  # noqa: D103
    ta_result = ta_service.perform_technical_analysis(sample_candlestick_data)

    latest = ta_result["latest_indicators"]

    # Basic sanity: latest dict must contain all indicator groups.
    expected_cols = TREND_COLS | MOMENTUM_COLS | VOLATILITY_COLS | VOLUME_COLS
    assert expected_cols.issubset(set(latest)), "Missing indicators in latest result"  # noqa: E501


def test_detect_selected_patterns_schema(sample_candlestick_data) -> None:  # noqa: D103
    patterns = ta_service.detect_selected_patterns(sample_candlestick_data)

    assert set(patterns) == {"detected_patterns"}
    # detected_patterns is a mapping even if empty
    assert isinstance(patterns["detected_patterns"], dict)