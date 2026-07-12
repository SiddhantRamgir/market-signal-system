def resample_ohlcv(df, timeframe="15min"):
    df_resampled = df.resample(timeframe).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    })

    return df_resampled.dropna()