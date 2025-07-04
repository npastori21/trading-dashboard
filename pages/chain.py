import pandas as pd
import numpy as np
import requests as r
import datetime
import streamlit as st
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh
from scipy.stats import norm
from bs4 import BeautifulSoup
from api import get_underlying_price, get_last_year_pricing, get_rfr, get_strike, get_vol, build_chain, calls_and_puts, build_chain_cached
from display import sell_strangle_payoff, plot_strangle_payoff

pd.options.plotting.backend = 'plotly'


st.set_page_config(
    page_title="Chain",
    page_icon="📈💵⛓️‍💥",
)



# st_autorefresh(interval=20 * 1000, key="auto-refresh")
# Initialize session state values
for key in ["ticker", "low_strike", "high_strike", "interval"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Input widgets with session state

API_KEY = st.secrets["API_KEY"]
st.session_state.ticker = st.text_input("Enter a Stock Ticker", value=st.session_state.ticker)
st.session_state.low_strike = st.text_input("Enter the Minimum Strike", value=st.session_state.low_strike)
st.session_state.high_strike = st.text_input("Enter the Maximum Strike", value=st.session_state.high_strike)
st.session_state.interval = st.text_input("Enter the Interval", value=st.session_state.interval)
st.session_state.date = st.text_input('Enter a Date: MM-DD-YYYY')

# Proceed if all required fields are filled
if all([
    st.session_state.ticker,
    st.session_state.low_strike,
    st.session_state.high_strike,
    st.session_state.interval,
    st.button('Get Chain')
]):
    refresh_requested = st.button("🔁 Refresh Now")
    fetch_data = refresh_requested or 'chain' not in st.session_state

    if fetch_data:
        try:
            chain = build_chain(
                st.session_state.ticker,
                API_KEY,
                float(st.session_state.low_strike),
                float(st.session_state.high_strike),
                float(st.session_state.interval)
            )
            st.session_state.chain = chain  # Store the chain
            st.session_state.last_refreshed = datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%I:%M:%S %p")
        except Exception as e:
            st.error(f"Failed to build chain: {e}")
            st.stop()
    else:
        chain = st.session_state.chain

    # Show when data was last updated
    if 'last_refreshed' in st.session_state:
        st.markdown(f"✅ **Data last updated at:** {st.session_state.last_refreshed}")

    # Extract calls/puts for expiration date
    if len(st.session_state.date) == 10:
        try:
            month = int(st.session_state.date[:2])
            day = int(st.session_state.date[3:5])
            year = int(st.session_state.date[6:])
            calls, puts = calls_and_puts(chain, month, day, year)

            st.dataframe(calls)
            st.dataframe(puts)
        except Exception as e:
            st.error(f"Failed to extract calls and puts: {e}")

