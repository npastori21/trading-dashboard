import pandas as pd
import datetime
from api.client import get

def get_underlying_price(ticker: str) -> float:
    try:
        data = get(f"/v2/symbols/{ticker}/series", {
            "bar_type": "minute",
            "bar_interval": "1",
            "extended": "true"
        })
        return data["series"][0]["close"]
    except Exception:
        return 0

def get_last_year_pricing(ticker: str) -> pd.DataFrame:
    """Fetch last year of daily closing prices for a ticker."""
    try:
        data = get(f"/v2/symbols/{ticker}/history", {
            "bar_type": "day",
            "bar_interval": "1",
            "extended": "true",
            "badj": "true",
            "dadj": "false"
        })

        pricing = pd.DataFrame(data["series"])
        pricing["time"] = pricing["time"].apply(datetime.date.fromtimestamp)
        pricing.index = pricing["time"]
        return pricing[["close"]].iloc[-253:]  # ~1 trading year
    except Exception as e:
        print(f"[ERROR] Failed to get historical pricing: {e}")
        return pd.DataFrame()