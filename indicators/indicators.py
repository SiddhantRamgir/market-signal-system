from ta.trend import MACD
from ta.momentum import RSIIndicator


def add_indicators(df):
    df = df.copy()

    df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()

    df["RSI"] = RSIIndicator(
        close=df["Close"],
        window=14
    ).rsi()

    macd = MACD(close=df["Close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    return df