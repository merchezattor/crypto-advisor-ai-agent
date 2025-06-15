from __future__ import annotations

"""FastAPI application exposing Crypto Advisor workflows via HTTP endpoints."""

import asyncio
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crypto_advisor.agent import load_environment
from crypto_advisor.workflows import (
    build_market_overview_app,
    build_technical_analysis_app,
)

# ---------------------------------------------------------------------------
# Pydantic response models
# ---------------------------------------------------------------------------


class AdvisorResponse(BaseModel):
    """Generic response schema containing the final LLM message."""

    message: str


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------


load_environment()
app = FastAPI(title="Crypto Advisor API", version="0.1.0")


async def _invoke_sync(app_callable, payload: dict[str, Any] | None = None) -> str:  # noqa: D401,E501
    """Run blocking LangGraph invocation in a worker thread."""

    payload = payload or {}
    result = await asyncio.to_thread(app_callable.invoke, payload)
    return result["messages"][-1].content


@app.get("/market-overview", response_model=AdvisorResponse, tags=["analysis"])
async def market_overview_endpoint() -> AdvisorResponse:  # noqa: D103
    try:
        message = await _invoke_sync(build_market_overview_app())
        return AdvisorResponse(message=message)
    except Exception as exc:  # pragma: no cover – runtime safeguard
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/technical-analysis", response_model=AdvisorResponse, tags=["analysis"])
async def technical_analysis_endpoint(symbol: str = "ETHUSDT") -> AdvisorResponse:  # noqa: D103
    try:
        message = await _invoke_sync(build_technical_analysis_app(symbol))
        return AdvisorResponse(message=message)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# Uvicorn entry helper
# ---------------------------------------------------------------------------


def run() -> None:  # pragma: no cover
    """Run a production-ready Uvicorn server if executed as a script."""

    import uvicorn  # local import to avoid mandatory dependency in pure-lib mode

    uvicorn.run("crypto_advisor.server:app", host="0.0.0.0", port=8000, reload=False) 