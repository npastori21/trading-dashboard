import streamlit as st
import pandas as pd
import datetime
import time
from utils.auth import check_auth
from api.chain_builder import build_chain

COOLDOWN_SECONDS = 10
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

check_auth()
# Optional: Customize the page
st.set_page_config(page_title="Options Chain Builder", layout="wide")
st.title("📊 Options Chain Visualizer")

# Cached wrapper for the chain builder
@st.cache_data(show_spinner="Loading option chain...")
def build_chain_cached(ticker, low_strike, high_strike, interval):
    return build_chain(ticker, low_strike, high_strike, interval)

# --- Initialize flag ---
if "submitted_chain_form" not in st.session_state:
    st.session_state.submitted_chain_form = False

# --- Form UI ---

ticker = st.text_input("Enter Ticker", value="NASDAQ:AAPL")
col1, col2, col3 = st.columns(3)
with col1:
    low_strike = st.number_input("Low Strike", value=180.0, step=1.0)
with col2:
    high_strike = st.number_input("High Strike", value=220.0, step=1.0)
with col3:
    interval = st.number_input("Strike Interval", value=5.0, step=1.0)


# --- Form Logic ---
def validate_strike_range(low, high):
    return high > low

def load_and_display_chain(ticker, low, high, interval):
    df = build_chain_cached(ticker, low, high, interval)
    if df.empty:
        st.warning("No data returned. Please check the ticker or try different strikes.")
        return None
    st.success(f"✅ Loaded option chain for {ticker}")
    return df

# --- On submit: build and store chain
if st.button("🔍 Build Chain"):
    now = time.time()
    elapsed = now - st.session_state.last_request_time
    if not validate_strike_range(low_strike, high_strike):
        st.error("⚠️ High Strike must be greater than Low Strike.")
    else:
        if elapsed < COOLDOWN_SECONDS:
            wait_time = int(COOLDOWN_SECONDS - elapsed)
            st.warning(f"Please wait {wait_time} seconds before submitting again.")
        else:
            try:
                chain_df = build_chain_cached(ticker, low_strike, high_strike, interval)
                st.session_state.last_request_time = now
            except Exception as e:
                chain_df = pd.DataFrame()
            if chain_df is not None and not chain_df.empty:
                st.session_state.chain_df = chain_df
            else:
                st.warning("No chain data found.")

# --- Show filters and tables only if chain is cached
if "chain_df" in st.session_state:
    chain_df = st.session_state.chain_df

    with st.container():
        st.subheader("📅 View Calls & Puts by Expiration")
        col4, _, _ = st.columns(3)
        with col4:
            future_exps = sorted(
                e for e in chain_df.index.unique()
                if pd.to_datetime(e) >= pd.to_datetime(datetime.datetime.now().date())
            )
            selected_exp = st.selectbox(
                "Expiration Date",
                future_exps,
                format_func=lambda d: d.strftime("%Y-%m-%d"),
                key="exp_filter"
            )

        calls = chain_df[(chain_df.index == selected_exp) & (chain_df["Option Type"] == "CALL")]
        puts = chain_df[(chain_df.index == selected_exp) & (chain_df["Option Type"] == "PUT")]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📞 Calls")
            st.dataframe(calls, use_container_width=True)
        with col2:
            st.subheader("📉 Puts")
            st.dataframe(puts, use_container_width=True)

