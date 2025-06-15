from __future__ import annotations

"""LangGraph-based workflows for Crypto Advisor.

This module defines two independent graphs:

* ``build_market_overview_app`` – Generates a high-level market overview.
* ``build_technical_analysis_app`` – Performs a technical analysis on a
  specific trading pair (currently ETH/USDT) and returns structured insights.

Each graph is compiled via `langgraph.StateGraph` and can be invoked just like
any other LangChain Runnable::

    app = build_market_overview_app()
    result = app.invoke({})

Both graphs share the same LLM/tooling stack; only the *prompt seed* differs.
"""

from typing import Any, Dict, List, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph

from crypto_advisor.agent import create_agent, load_environment
from crypto_advisor.prompts import market_overview_query

from crypto_advisor.providers.binance import fetch_binance_chart
from crypto_advisor.services import ta_service


class GraphState(TypedDict):
    """Minimal state passed between graph nodes."""

    messages: List[BaseMessage]
    candles: list | None
    indicators: dict | None
    volatility: dict | None


# ---------------------------------------------------------------------------
# Shared building blocks
# ---------------------------------------------------------------------------


def _build_agent_runnable() -> Runnable[[GraphState], GraphState]:  # type: ignore[type-arg]
    """Wrap the existing LangChain agent into a Runnable interface."""

    agent = create_agent()

    def _run(state: GraphState) -> GraphState:  # noqa: WPS430
        response = agent.invoke(state["messages"])
        return {"messages": state["messages"] + [AIMessage(content=response)]}

    return _run  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Workflow builders
# ---------------------------------------------------------------------------


def _build_app(prompt_messages: List[tuple[str, str]]) -> Runnable[[Dict[str, Any]], Dict[str, Any]]:  # noqa: E501
    """Internal helper to assemble a graph for a given seed prompt."""

    # Node 1 – seed the conversation with the predefined prompt.
    def seed(_: GraphState) -> GraphState:  # noqa: D401
        human_messages = [HumanMessage(content=msg) for _role, msg in prompt_messages]
        return {"messages": human_messages}

    # Create graph.
    graph: StateGraph[GraphState] = StateGraph(GraphState)
    graph.add_node("seed", seed)

    # Agent node.
    graph.add_node("agent", _build_agent_runnable())

    # Linear flow: seed → agent → END.
    graph.add_edge("seed", "agent")
    graph.add_edge("agent", END)

    return graph.compile()


def build_market_overview_app() -> Runnable[[Dict[str, Any]], Dict[str, Any]]:  # noqa: D103
    load_environment()
    return _build_app(market_overview_query())


def build_technical_analysis_app(symbol: str = "ETHUSDT") -> Runnable[[Dict[str, Any]], Dict[str, Any]]:  # noqa: D103
    """Build a graph that performs a full technical analysis for the given pair."""

    load_environment()

    def seed(_: GraphState) -> GraphState:  # noqa: D401
        prompt = f"Perform full technical analysis for {symbol} pair to give insights for investor."
        return {
            "messages": [HumanMessage(content=prompt)],
            "candles": None,
            "indicators": None,
            "volatility": None,
        }

    def fetch(_: GraphState) -> GraphState:  # noqa: D401
        candles = fetch_binance_chart(symbol, "4h", 100)
        return {"candles": candles}

    def calc_indicators(state: GraphState) -> GraphState:  # noqa: D401
        indicators = ta_service.perform_technical_analysis(state["candles"])["latest_indicators"]  # type: ignore[index]
        return {"indicators": indicators}

    def calc_vol(state: GraphState) -> GraphState:  # noqa: D401
        volatility = ta_service.calculate_volatility_index(state["candles"])
        return {"volatility": volatility}

    agent_runnable = _build_agent_runnable()

    graph: StateGraph[GraphState] = StateGraph(GraphState)
    graph.add_node("seed", seed)
    graph.add_node("fetch", fetch)
    graph.add_node("indicators", calc_indicators)
    graph.add_node("vol", calc_vol)
    graph.add_node("agent", agent_runnable)

    # Edges
    graph.add_edge("seed", "fetch")
    graph.add_edge("fetch", "indicators")
    graph.add_edge("indicators", "vol")
    graph.add_edge("vol", "agent")
    graph.add_edge("agent", END)

    return graph.compile() 