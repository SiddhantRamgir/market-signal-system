import sys
from pathlib import Path
from config import settings

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ingestion.fetch_data import fetch_1m_data
from indicators.resample import resample_ohlcv
from indicators.indicators import add_indicators
from signals.signal_engine import generate_signal


SYMBOLS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "BSE Sensex": "^BSESN",
    "Ireland ISEQ": "^ISEQ"
}


def filter_latest_trading_day(df):
    latest_timestamp = df.index.max()
    latest_date = latest_timestamp.date()

    return df[df.index.date == latest_date]


def filter_window(df, window):
    if window == "Full active day":
        return df

    latest_timestamp = df.index.max()

    if window == "1 hour":
        start_time = latest_timestamp - pd.Timedelta(hours=1)
    elif window == "3 hours":
        start_time = latest_timestamp - pd.Timedelta(hours=3)
    elif window == "6 hours":
        start_time = latest_timestamp - pd.Timedelta(hours=6)
    else:
        return df

    return df[df.index >= start_time]


st.set_page_config(
    page_title="Intraday Market Signal System",
    layout="wide"
)

st.title("Intraday Market Signal System")

st.caption(
    f"Environment: {settings.app_env.upper()} | "
    f"Data period: {settings.default_period} | "
    f"Source interval: {settings.default_interval}"
)

st.write("Intraday index signal dashboard using Yahoo Finance OHLC data.")

st.divider()

col_a, col_b, col_c = st.columns(3)

with col_a:
    selected_index = st.selectbox("Select Index", list(SYMBOLS.keys()))

with col_b:
    selected_timeframe = st.selectbox("Signal Timeframe", ["15min", "30min"])

with col_c:
    selected_window = st.selectbox(
        "Chart Window",
        ["Full active day", "1 hour", "3 hours", "6 hours"]
    )

symbol = SYMBOLS[selected_index]

if st.button("Refresh Data"):
    st.rerun()

st.divider()

# Fetch 5 days for proper indicator warm-up
df_1m = fetch_1m_data(symbol, period="5d")

if df_1m.empty:
    st.error("No data returned from Yahoo Finance.")
    st.stop()

df_resampled = resample_ohlcv(df_1m, selected_timeframe)

if df_resampled.empty:
    st.error("No resampled data available.")
    st.stop()

df_indicators = add_indicators(df_resampled)

result = generate_signal(df_indicators)

if result["signal"] == "NO DATA":
    st.warning("Not enough indicator data yet.")
    st.stop()

# Filter chart to latest active trading day only
df_latest_day = filter_latest_trading_day(df_indicators)

# Then filter by selected chart window
df_chart = filter_window(df_latest_day, selected_window)

if df_chart.empty:
    st.warning("No chart data available for selected window.")
    st.stop()

latest_chart_time = df_chart.index.max()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Signal", result["signal"])
col2.metric("Confidence Score", result["confidence_score"])
col3.metric("Latest Close", result["close"])
col4.metric("Timeframe", selected_timeframe)

st.write(
    f"RSI: {result['rsi']} | "
    f"MACD: {result['macd']} | "
    f"MACD Signal: {result['macd_signal']} | "
    f"EMA20: {result['ema20']} | "
    f"EMA50: {result['ema50']}"
)

st.caption(f"Chart showing: {selected_window} | Latest candle: {latest_chart_time}")

st.divider()

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df_chart.index,
        open=df_chart["Open"],
        high=df_chart["High"],
        low=df_chart["Low"],
        close=df_chart["Close"],
        name="OHLC"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_chart.index,
        y=df_chart["EMA20"],
        mode="lines",
        name="EMA20"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_chart.index,
        y=df_chart["EMA50"],
        mode="lines",
        name="EMA50"
    )
)

fig.update_layout(
    title=f"{selected_index} ({symbol}) - {selected_timeframe} Chart - {selected_window}",
    xaxis_title="Time",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False,
    height=650
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

with st.expander("Show latest indicator data"):
    st.dataframe(
        df_chart[
            ["Open", "High", "Low", "Close", "EMA20", "EMA50", "RSI", "MACD", "MACD_SIGNAL"]
        ].tail(30),
        use_container_width=True
    )