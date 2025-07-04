from api.price import get_last_year_pricing

def get_vol(ticker: str) -> float:
    """Calculate annualized historical volatility using daily returns."""
    price_data = get_last_year_pricing(ticker)
    if price_data.empty:
        return 0.3  # fallback

    price_data["returns"] = price_data["close"].pct_change()
    return price_data["returns"].std() * (252 ** 0.5)