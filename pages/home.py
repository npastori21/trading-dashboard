import streamlit as st
import datetime
from utils.auth import check_password



st.set_page_config(page_title="Home", page_icon="🪙")
check_password()

st.title("📈 Delta Desk")
st.markdown("---")

st.markdown(
    """
    Welcome to **Delta Desk** – a streamlined tool for retail and professional traders looking to visualize
    options strategies and analyze live options chain data.

    ### 🚀 What You Can Do:
    - **Simulate a Sell Strangle Strategy** using customizable strike prices, premiums, and quantities.
    - **Fetch and Explore Real-Time Option Chains** from supported tickers with adjustable strike intervals and expiration dates.
    - **Evaluate Profit & Loss** across a range of expiration prices using interactive Plotly charts.

    ---
    ### 🧭 Navigation:
    Use the **sidebar** on the left to:
    - Pull live market data from **Chain**
    - Construct **Strangle** strategies
    - Read the full **Usage Guide**

    ---
    ### 🛡️ Secure API Integration:
    This app is powered by a third-party financial data API. Your API key is stored securely using **Streamlit Secrets**.
    """
)

year = datetime.datetime.now().year
st.markdown(
    f"<p style='text-align: center; font-size: 0.85em; color: gray; padding-top: 2em;'>"
    f"© {year} Nicholas Pastori. All rights reserved."
    f"</p>",
    unsafe_allow_html=True
)