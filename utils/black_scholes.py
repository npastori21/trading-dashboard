import numpy as np
import pandas as pd
from scipy.stats import norm
import datetime

def black_scholes(rfr, vol, strike, spot, time, option_type):
    """Compute Black-Scholes price for a European call or put."""
    if time <= 0:
        return max(spot - strike, 0) if option_type == "CALL" else max(strike - spot, 0)

    d1 = (np.log(spot / strike) + (rfr + 0.5 * vol**2) * time) / (vol * np.sqrt(time))
    d2 = d1 - vol * np.sqrt(time)

    if option_type == "CALL":
        return spot * norm.cdf(d1) - strike * np.exp(-rfr * time) * norm.cdf(d2)
    else:
        return strike * np.exp(-rfr * time) * norm.cdf(-d2) - spot * norm.cdf(-d1)

def build_black_scholes(row, spot, vol, rfr, historical=True):
    """Vectorized wrapper for DataFrame row — computes either historical or implied BS price."""
    if not historical:
        vol = row.get("implied_volatility", vol)

    expiration = row["expiration"]
    strike = row["strike_price"]
    option_type = row["type"]

    time = (expiration - datetime.datetime.now()).total_seconds() / (365 * 86400)
    if time < 0:
        time = 0

    return round(black_scholes(rfr, vol, strike, spot, time, option_type), 2)
