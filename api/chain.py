import pandas as pd
from api.client import get
from utils.logger import log_error

def get_strike(ticker: str, strike: float) -> pd.DataFrame:
    """Fetch option chain data for a given ticker and strike price."""
    try:
        data = get("/v2/options/strike", {
            "code": ticker,
            "s": strike,
            "sortBy": "type",
            "sort": "asc"
        })
        chain = pd.DataFrame(data["data"]).sort_values(by="expiration")
        chain["expiration"] = pd.to_datetime(chain["expiration"].astype(str))
        chain.index = chain["expiration"]
        chain["ticker"] = ticker
        return chain
    except Exception as e:
        print(f"[ERROR] Failed to fetch strike {strike} for {ticker}: {e}")
        log_error(e)
        return pd.DataFrame()