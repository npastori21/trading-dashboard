import streamlit as st
from display import home_sidebar



home_sidebar()

st.set_page_config(page_title="Home", page_icon="🪙")

st.title("📈 Trading Dashboard")
st.markdown("---")

st.markdown(
    """
    Welcome to the **Trading Dashboard** – a streamlined tool for retail and professional traders looking to visualize
    options strategies and analyze live options chain data.

    ### 🚀 What You Can Do:
    - **Simulate a Sell Strangle Strategy** using customizable strike prices, premiums, and quantities.
    - **Fetch and Explore Real-Time Option Chains** from supported tickers with adjustable strike intervals and expiration dates.
    - **Evaluate Profit & Loss** across a range of expiration prices using interactive Plotly charts.

    ---
    ### 🧭 Navigation:
    Use the **sidebar** on the left to:
    - Pull live market data from **Chain**
    - Read the full **Usage Guide**

    ---
    ### 🛡️ Secure API Integration:
    This app is powered by a third-party financial data API. Your API key is stored securely using **Streamlit Secrets**.
    """
)