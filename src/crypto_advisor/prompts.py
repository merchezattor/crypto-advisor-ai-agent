from __future__ import annotations

"""Predefined prompt templates for Crypto Advisor workflows."""

from typing import List, Tuple

__all__: list[str] = [
    "market_overview_query",
    "technical_analysis_query",
]


def market_overview_query() -> List[Tuple[str, str]]:  # noqa: D401
    """Return market-overview seed prompt."""

    return [
        (
            "human",
            (
                "Provide a global market overview for today, using historical trends "
                "from the last 60 days as context. Summarize the current state of the "
                "crypto market, including total market cap trends, Bitcoin dominance "
                "shifts, and key volume movements. Assess the Fear & Greed Index and "
                "explain whether the sentiment aligns with price action. Identify any "
                "major anomalies or unusual market behavior in the last few days. "
                "Evaluate whether capital is flowing into BTC or altcoins and describe "
                "the implications. Summarize potential scenarios for the market in the "
                "short term (bullish, bearish, or uncertain) based on current data. "
                "Do NOT just repeat numbers—provide clear, investor-focused insights "
                "backed by data."
            ),
        ),
    ]


def technical_analysis_query() -> List[Tuple[str, str]]:
    """Return technical-analysis seed prompt for ETH/USDT."""

    return [
        (
            "human",
            (
                "Fetch the last 100 4-hour candlesticks for ETHUSDT. "
                "Perform a full technical analysis, including RSI, MACD, Moving Averages, "
                "Bollinger Bands, and Volume-based indicators. Additionally, detect any "
                "potential chart patterns such as Double Top, Head and Shoulders, Cup and "
                "Handle, or Triangles. Do NOT just list the values—analyze how these "
                "indicators interact and what they signal together. If conflicting "
                "signals appear, explain which indicator is more reliable in the current "
                "market. Summarize whether BTC is currently in a bullish, bearish, or "
                "uncertain phase based on the combined results. Provide a short-term "
                "market outlook, highlighting key levels to watch for breakouts or "
                "reversals. Also give probability of bullish and bearish scenarios."
            ),
        ),
    ] 