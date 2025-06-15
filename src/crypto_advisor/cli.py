from __future__ import annotations

"""Command-line interface for Crypto Advisor workflows."""

import argparse
import sys

from crypto_advisor.main import run_agent


def _build_parser() -> argparse.ArgumentParser:  # noqa: D401
    parser = argparse.ArgumentParser(description="Run Crypto Advisor analysis workflows from the command line.")
    parser.add_argument(
        "--query-type",
        choices=["market_overview", "technical_analysis"],
        default="market_overview",
        help="Select analysis workflow.",
    )
    parser.add_argument(
        "--symbol",
        default="ETHUSDT",
        help="Trading pair symbol (technical_analysis only).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=60,
        help="Number of days for market overview (market_overview only).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:  # pragma: no cover
    """Parse CLI arguments and invoke the requested workflow."""

    argv = argv if argv is not None else sys.argv[1:]
    parser = _build_parser()
    args = parser.parse_args(argv)

    response = run_agent(
        query_type=args.query_type,
        symbol=args.symbol,
        days=args.days,
    )
    print(response)


if __name__ == "__main__":  # pragma: no cover
    main() 