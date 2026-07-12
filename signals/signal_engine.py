import pandas as pd

from monitoring.logging_config import get_logger


logger = get_logger(__name__)


def generate_signal(df: pd.DataFrame) -> dict:
    required_columns = {
        "Close",
        "EMA20",
        "EMA50",
        "RSI",
        "MACD",
        "MACD_SIGNAL",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        logger.error(
            "signal_input_schema_invalid",
            extra={
                "missing_columns": sorted(missing_columns),
                "available_columns": list(df.columns),
            },
        )

        return {
            "signal": "NO DATA",
            "confidence_score": 0,
        }

    clean_df = df.dropna(subset=list(required_columns))

    if clean_df.empty:
        logger.warning("signal_input_empty")

        return {
            "signal": "NO DATA",
            "confidence_score": 0,
        }

    latest = clean_df.iloc[-1]
    score = 0

    ema_score = 30 if latest["EMA20"] > latest["EMA50"] else -30
    score += ema_score

    if latest["RSI"] > 55:
        rsi_score = 25
    elif latest["RSI"] < 45:
        rsi_score = -25
    else:
        rsi_score = 0

    score += rsi_score

    macd_score = (
        25
        if latest["MACD"] > latest["MACD_SIGNAL"]
        else -25
    )

    score += macd_score

    if score >= 50:
        signal = "BUY"
    elif score <= -50:
        signal = "SELL"
    else:
        signal = "HOLD"

    result = {
        "signal": signal,
        "confidence_score": score,
        "close": round(float(latest["Close"]), 2),
        "rsi": round(float(latest["RSI"]), 2),
        "macd": round(float(latest["MACD"]), 4),
        "macd_signal": round(float(latest["MACD_SIGNAL"]), 4),
        "ema20": round(float(latest["EMA20"]), 2),
        "ema50": round(float(latest["EMA50"]), 2),
    }

    logger.info(
        "signal_generated",
        extra={
            "signal": signal,
            "confidence_score": score,
            "ema_score": ema_score,
            "rsi_score": rsi_score,
            "macd_score": macd_score,
            "close": result["close"],
        },
    )

    return result