# Crypto Advisor AI-agent

🚀 **An advanced AI-powered market analysis agent designed to provide deep insights into Bitcoin (BTC) and the overall cryptocurrency market.** 

This bot combines **real-time market data, historical trends, technical indicators, and sentiment analysis** to detect patterns, anomalies, and potential market opportunities.

### 🔍 Purpose

This AI agent is built to **go beyond basic market data** by offering **actionable insights** into BTC's price action, sentiment trends, and overall market dynamics. Instead of just listing numbers, it **interprets data** to highlight key market shifts, potential trading signals, and risk factors.

It can answer questions like:
- *"Is BTC overbought or oversold based on technical indicators?"*
- *"How has market sentiment changed in the last 60 days?"*
- *"Are we in an accumulation or distribution phase?"*

## 🛠️ Features & Capabilities
- **📊 Technical Analysis** – RSI, MACD, Moving Averages, Trend Patterns
- **📈 Market Trends** – BTC Dominance, Total Market Cap, Volume Movements
- **📰 Sentiment Analysis** – Fear & Greed Index, Market Psychology Insights
- **📅 Historical Analysis** – Compare past & present market conditions
- **⚡ Real-Time Data** – Fetch live prices, trading volume, and liquidity metrics

## 🔗 Data Sources & Technologies
- **🛠 LangChain** – AI agent framework for intelligent tool selection
- **🤖 OpenAI GPT-4 Turbo** – Advanced market reasoning & analysis
- **📡 APIs Integrated**:
  - **CoinMarketCap API** – Market cap, BTC dominance, liquidity data
  - **Binance API** – Real-time & historical price charts
  - **Fear & Greed Index API** – Market sentiment tracking
- **📊 Technical Indicators** – `ta` Python library for RSI, MACD, SMAs

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Poetry (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lang-chain-ai-agent.git
   cd lang-chain-ai-agent
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Run the pandas-ta patch to fix compatibility issues:
   ```bash
   poetry run fix-pandas-ta
   ```

4. Create a `.env` file with your API keys (see `.env.example` for required keys)

5. Run the agent:
   ```bash
   poetry run python main.py
   ```

## 🚀 Future Plans
- 📰 **News Sentiment Analysis** – Crypto news & Twitter data integration
- 🏦 **On-Chain Metrics** – Whale activity, exchange inflows/outflows
- 📈 **Multi-Coin Support** – Expanding analysis beyond BTC

---

This bot is designed for **traders, analysts, and enthusiasts** looking to understand **Bitcoin's market trends in real-time** and gain **data-driven insights** into potential opportunities.