# Crypto Advisor

A lightweight, self-hosted service that generates data-driven insights for the cryptocurrency market.  It exposes two analysis workflows via a REST API powered by FastAPI and LangGraph.

## Endpoints

| Method | URL                  | Description                                |
|--------|----------------------|--------------------------------------------|
| GET    | /market-overview     | Returns a high-level market overview.      |
| GET    | /technical-analysis  | Performs a technical study of ETH/USDT.    |

Both routes respond with a JSON object:

```json
{
  "message": "…LLM response…"
}
```

## Quick start

```bash
# 1. Install Poetry & project deps
poetry install

# 2. Add your credentials to .env (at least OPENAI_API_KEY)
cp .env.example .env && $EDITOR .env

# 3. Launch the API server
poetry run crypto-advisor-api  # runs uvicorn on 0.0.0.0:8000

# 4. Open interactive docs
open http://localhost:8000/docs
```

Optional CLI usage (kept for one-off runs):

```bash
poetry run crypto-advisor  # prints market overview to stdout
```

## Testing

```bash
# unit tests
poetry run pytest

# include integration tests (requires internet)
poetry run pytest --run-integration
```

## Tech stack

* Python ≥ 3.10
* FastAPI + Uvicorn
* LangGraph + LangChain tools
* pandas / ta / pandas-ta for indicator calculations

## License

MIT