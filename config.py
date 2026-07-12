import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Loads values from .env when running locally.
# Inside Docker or Azure, real environment variables are overrides them.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_env: str
    log_level: str
    default_period: str
    default_interval: str
    default_timeframe: str


def load_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        default_period=os.getenv("DEFAULT_PERIOD", "5d"),
        default_interval=os.getenv("DEFAULT_INTERVAL", "1m"),
        default_timeframe=os.getenv("DEFAULT_TIMEFRAME", "15min"),
    )


settings = load_settings()