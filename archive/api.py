import pandas as pd
import numpy as np
import requests as r
import datetime
from scipy.stats import norm
from bs4 import BeautifulSoup
import streamlit as st

def get_underlying_price(ticker, API_KEY):
    url = f'https://insightsentry.p.rapidapi.com/v2/symbols/{ticker}/series'
    headers = {
        'x-rapidapi-key': API_KEY,
	    'x-rapidapi-host': 'insightsentry.p.rapidapi.com'
    }
    querystring = {"bar_type":"minute","bar_interval":"1","extended":"true"}
    response = r.get(url, headers=headers, params=querystring)
    try:
        return response.json()['series'][0]['close']
    except:
        return 0
    
def get_strike(ticker, API_KEY, strike):
    url = f'https://insightsentry.p.rapidapi.com/v2/options/strike'
    headers = {
        'x-rapidapi-key': API_KEY,
	    'x-rapidapi-host': 'insightsentry.p.rapidapi.com'
    }
    querystring = {f"code":{ticker},"s":{strike},"sortBy":"type","sort":"asc"}
    response = r.get(url, headers=headers, params=querystring)
    chain = pd.DataFrame(response.json()['data']).sort_values(by='expiration')
    chain['expiration'] = pd.to_datetime(chain['expiration'].astype(str))
    chain.index = chain['expiration']
    chain['ticker'] = ticker
    return chain

def build_chain(ticker, API_KEY, low_strike, high_strike, interval):
    spot = get_underlying_price(ticker, API_KEY)
    annual_vol = get_vol(API_KEY, ticker)
    strike = low_strike
    rfr = get_rfr()
    to_chain = []
    while strike <= high_strike:
        to_chain.append(get_strike(ticker, API_KEY, strike))
        strike += interval
    chain = pd.concat(to_chain)
    chain.drop('theoretical_price', axis=1, inplace=True)
    chain['BS-Historical'] = chain.apply(build_black_scholes, args=(spot, annual_vol, rfr, True), axis=1)
    chain['BS-IV'] = chain.apply(build_black_scholes, args=(spot, annual_vol, rfr, False), axis=1)
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
    return chain[["Ticker", "Option Type", "Ask Price", "Bid Price", "BS (Historical Volatility)","BS (Implied Volatility)","Implied Volatility", 
                       "Delta", "Gamma", "Rho", "Strike Price", "Theta", "Vega"]]

def get_last_year_pricing(API_KEY, ticker):
    url = f"https://insightsentry.p.rapidapi.com/v2/symbols/{ticker}/history"

    querystring = {"bar_type":"day","bar_interval":"1","extended":"true","badj":"true","dadj":"false"}

    headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "insightsentry.p.rapidapi.com"
    }

    response = r.get(url, headers=headers, params=querystring)
    pricing = pd.DataFrame(response.json()['series'])
    pricing['time'] = pricing['time'].apply(datetime.date.fromtimestamp)
    pricing.index = pricing['time']
    return pd.DataFrame(pricing['close'].iloc[-253:])

def get_vol(API_KEY, ticker):
    price_data = get_last_year_pricing(API_KEY, ticker)
    price_data['returns'] = (price_data['close'] - price_data['close'].shift(1))/price_data['close']
    price_data.dropna(inplace=True)
    return price_data['returns'].std()

def get_rfr():  
    treasury_site = r.get('https://fred.stlouisfed.org/series/DGS10').text
    soup = BeautifulSoup(treasury_site, features='html.parser') 
    return float(
            (soup.find('div', id='container')
                .find('div', id='main-content-column')
                .find('div', class_='row series-attributes')
                .find('p', class_='mb-2')
                .find_next('span')).text
        )/100

def black_scholes(rfr, vol, strike, spot, time, type):
    if time <= 0:
        if type == "CALL":
            return max(spot - strike, 0)
        else:
            return max(strike - spot, 0)
    d1 = (np.log(spot/strike) + ((rfr + .5 * vol**2) * time))/ (np.sqrt(time) * vol)
    d2 = (d1 - (vol * np.sqrt(time)))
    if type == 'CALL':
        return (spot * norm.cdf(d1)) - (strike * np.exp(-rfr * time) * norm.cdf(d2))
    else:
        return (strike * np.exp(-rfr * time) * norm.cdf(-d2)) - (spot * norm.cdf(-d1))
    
def build_black_scholes(row, spot, vol, rfr, historical):
    if not historical:
        vol = row['implied_volatility']
    
    expiration = row['expiration']
    strike = row['strike_price']
    t = row['type']
    current = datetime.datetime.now()
    time = (expiration - current).total_seconds() / 86400
    return round(black_scholes(rfr, vol, strike, spot, time/365, t), 2)

def calls_and_puts(chain, month, day, year):
    return chain[(chain.index == datetime.datetime(year,month,day)) & (chain['Option Type'] == 'CALL')], chain[(chain.index == datetime.datetime(year,month,day)) & (chain['Option Type'] == 'PUT')]


@st.cache_data(show_spinner="Loading option chain...")
def build_chain_cached(ticker, api_key, low_strike, high_strike, interval):
    return build_chain(ticker, api_key, low_strike, high_strike, interval)
