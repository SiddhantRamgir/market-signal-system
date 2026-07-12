import pandas as pd

from signals.signal_engine import generate_signal


def create_signal_dataframe(
    *,
    close: float = 100.0,
    ema20: float,
    ema50: float,
    rsi: float,
    macd: float,
    macd_signal: float,
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Close": close,
                "EMA20": ema20,
                "EMA50": ema50,
                "RSI": rsi,
                "MACD": macd,
                "MACD_SIGNAL": macd_signal,
            }
        ]
    )


def test_generate_buy_signal() -> None:
    df = create_signal_dataframe(
        ema20=105,
        ema50=100,
        rsi=60,
        macd=2,
        macd_signal=1,
    )

    result = generate_signal(df)

    assert result["signal"] == "BUY"
    assert result["confidence_score"] == 80


def test_generate_sell_signal() -> None:
    df = create_signal_dataframe(
        ema20=95,
        ema50=100,
        rsi=35,
        macd=-2,
        macd_signal=-1,
    )

    result = generate_signal(df)

    assert result["signal"] == "SELL"
    assert result["confidence_score"] == -80


def test_generate_hold_signal() -> None:
    df = create_signal_dataframe(
        ema20=105,
        ema50=100,
        rsi=50,
        macd=1,
        macd_signal=2,
    )

    result = generate_signal(df)

    assert result["signal"] == "HOLD"
    assert result["confidence_score"] == 5


def test_generate_no_data_when_dataframe_is_empty() -> None:
    df = pd.DataFrame(
        columns=[
            "Close",
            "EMA20",
            "EMA50",
            "RSI",
            "MACD",
            "MACD_SIGNAL",
        ]
    )

    result = generate_signal(df)

    assert result["signal"] == "NO DATA"
    assert result["confidence_score"] == 0


def test_generate_no_data_when_schema_is_invalid() -> None:
    df = pd.DataFrame(
        [
            {
                "Close": 100,
                "RSI": 50,
            }
        ]
    )

    result = generate_signal(df)

    assert result["signal"] == "NO DATA"