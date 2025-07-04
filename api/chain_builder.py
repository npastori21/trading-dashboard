import pandas as pd
from api.chain import get_strike
from api.price import get_underlying_price
from api.vol import get_vol
from api.rates import get_rfr
from utils.black_scholes import build_black_scholes

def frange(start: float, stop: float, step: float):
    while start <= stop:
        yield round(start, 2)
        start += step

def build_chain(ticker: str, low_strike: float, high_strike: float, interval: float) -> pd.DataFrame:
    spot = get_underlying_price(ticker)
    annual_vol = get_vol(ticker)
    rfr = get_rfr()

    all_strikes = list(frange(low_strike, high_strike, interval))
    chain_frames = [get_strike(ticker, s) for s in all_strikes]
    chain = pd.concat(chain_frames)

    chain.drop(columns=["theoretical_price"], errors="ignore", inplace=True)

    chain["BS (Historical Volatility)"] = chain.apply(
        build_black_scholes, args=(spot, annual_vol, rfr, True), axis=1)

    chain["BS (Implied Volatility)"] = chain.apply(
        build_black_scholes, args=(spot, annual_vol, rfr, False), axis=1)

    chain.columns = [
        "Ask Price",
        "Bid Price",
        "Delta",
        "Gamma",
        "Expiration",
        "Implied Volatility",
        "Option Type",
        "Rho",
        "Strike Price",
        "Theta",
        "Vega",
        "Ticker",
        "BS (Historical Volatility)",
        "BS (Implied Volatility)"
    ]
    chain.index.name = 'Expiration'
    return chain[["Ticker", "Strike Price", "Ask Price", "Bid Price", "BS (Historical Volatility)","BS (Implied Volatility)","Implied Volatility", 
                       "Delta", "Gamma", "Rho", "Option Type", "Theta", "Vega"]]
