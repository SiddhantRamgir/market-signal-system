import pandas as pd
import pytest

from indicators.resample import resample_ohlcv


@pytest.fixture
def one_minute_data() -> pd.DataFrame:
    index = pd.date_range(
        start="2026-05-20 09:30:00",
        periods=30,
        freq="1min",
        tz="UTC",
    )

    base_prices = list(range(100, 130))

    return pd.DataFrame(
        {
            "Open": base_prices,
            "High": [price + 1 for price in base_prices],
            "Low": [price - 1 for price in base_prices],
            "Close": [price + 0.5 for price in base_prices],
            "Volume": [10] * 30,
        },
        index=index,
    )


def test_resample_creates_two_fifteen_minute_candles(
    one_minute_data: pd.DataFrame,
) -> None:
    result = resample_ohlcv(
        one_minute_data,
        timeframe="15min",
    )

    assert len(result) == 2


def test_resample_calculates_correct_first_candle(
    one_minute_data: pd.DataFrame,
) -> None:
    result = resample_ohlcv(
        one_minute_data,
        timeframe="15min",
    )

    first_candle = result.iloc[0]

    assert first_candle["Open"] == 100
    assert first_candle["High"] == 115
    assert first_candle["Low"] == 99
    assert first_candle["Close"] == 114.5
    assert first_candle["Volume"] == 150