from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from indicators.indicators import add_indicators
from indicators.resample import resample_ohlcv
from ingestion.fetch_data import fetch_1m_data
from monitoring.logging_config import get_logger
from signals.signal_engine import generate_signal


logger = get_logger(__name__)


SYMBOLS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "BSE Sensex": "^BSESN",
    "Ireland ISEQ": "^ISEQ",
}

TIMEFRAME = "15min"
OUTPUT_PATH = Path("data/latest_signals.csv")


def run_pipeline() -> pd.DataFrame:
    results = []

    logger.info(
        "signal_pipeline_started",
        extra={
            "symbol_count": len(SYMBOLS),
            "timeframe": TIMEFRAME,
        },
    )

    for index_name, symbol in SYMBOLS.items():
        logger.info(
            "index_processing_started",
            extra={
                "index_name": index_name,
                "symbol": symbol,
            },
        )

        df_1m = fetch_1m_data(symbol)

        if df_1m.empty:
            logger.warning(
                "index_skipped_no_market_data",
                extra={
                    "index_name": index_name,
                    "symbol": symbol,
                },
            )
            continue

        df_resampled = resample_ohlcv(df_1m, TIMEFRAME)

        if df_resampled.empty:
            logger.warning(
                "index_skipped_no_resampled_data",
                extra={
                    "index_name": index_name,
                    "symbol": symbol,
                },
            )
            continue

        df_indicators = add_indicators(df_resampled)
        result = generate_signal(df_indicators)

        if result["signal"] == "NO DATA":
            logger.warning(
                "index_skipped_no_signal",
                extra={
                    "index_name": index_name,
                    "symbol": symbol,
                },
            )
            continue

        result.update(
            {
                "index_name": index_name,
                "symbol": symbol,
                "timeframe": TIMEFRAME,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    if results_df.empty:
        logger.error("signal_pipeline_completed_without_results")
        return results_df

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(OUTPUT_PATH, index=False)

    logger.info(
        "signal_pipeline_completed",
        extra={
            "signals_generated": len(results_df),
            "output_path": str(OUTPUT_PATH),
        },
    )

    return results_df


if __name__ == "__main__":
    output = run_pipeline()

    if not output.empty:
        print(output)