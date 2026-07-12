# Intraday Market Signal System

A containerised intraday market analytics application that processes delayed
Yahoo Finance OHLCV data and generates rule-based BUY, SELL, or HOLD signals.

The project is being developed as a practical exercise in application
engineering, cloud deployment, observability, CI/CD, infrastructure automation,
and production support.

## Current capabilities

- Downloads 1-minute OHLCV index data from Yahoo Finance
- Resamples data into 15-minute and 30-minute candles
- Calculates EMA20, EMA50, RSI, and MACD
- Generates scoring-based BUY, SELL, or HOLD signals
- Supports multiple international market indices
- Displays signals and candlestick charts through Streamlit
- Produces structured JSON application logs
- Includes automated unit tests
- Runs locally using Docker and Docker Compose
- Includes application health monitoring and restart configuration

## Current indices

- S&P 500
- Nasdaq Composite
- Dow Jones Industrial Average
- BSE Sensex
- Ireland ISEQ

## Architecture

```text
Yahoo Finance
      |
      v
1-minute OHLCV ingestion
      |
      v
Data validation
      |
      v
15-minute / 30-minute resampling
      |
      v
EMA, RSI and MACD calculations
      |
      v
Rule-based signal engine
      |
      v
Streamlit dashboard