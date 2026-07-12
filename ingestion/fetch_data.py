import pandas as pd
import yfinance as yf

from config import settings
from monitoring.logging_config import get_logger


logger = get_logger(__name__)


def fetch_1m_data(
    symbol: str,
    period: str | None = None,
    interval: str | None = None,
) -> pd.DataFrame:
    selected_period = period or settings.default_period
    selected_interval = interval or settings.default_interval

    logger.info(
        "market_data_fetch_started",
        extra={
            "symbol": symbol,
            "period": selected_period,
            "interval": selected_interval,
        },
    )

    try:
        df = yf.download(
            tickers=symbol,
            period=selected_period,
            interval=selected_interval,
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df.empty:
            logger.warning(
                "market_data_empty",
                extra={
                    "symbol": symbol,
                    "period": selected_period,
                    "interval": selected_interval,
                },
            )
            return pd.DataFrame()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        required_columns = {"Open", "High", "Low", "Close", "Volume"}
        missing_columns = required_columns.difference(df.columns)

        if missing_columns:
            logger.error(
                "market_data_schema_invalid",
                extra={
                    "symbol": symbol,
                    "missing_columns": sorted(missing_columns),
                    "available_columns": list(df.columns),
                },
            )
            return pd.DataFrame()

        df = df.dropna(
            subset=["Open", "High", "Low", "Close"]
        )

        logger.info(
            "market_data_fetch_completed",
            extra={
                "symbol": symbol,
                "row_count": len(df),
                "first_timestamp": df.index.min(),
                "last_timestamp": df.index.max(),
            },
        )

        return df

    except Exception as error:
        logger.exception(
            "market_data_fetch_failed",
            extra={
                "symbol": symbol,
                "period": selected_period,
                "interval": selected_interval,
                "error": str(error),
            },
        )

        return pd.DataFrame()