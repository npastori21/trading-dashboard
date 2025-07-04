import streamlit as st

chain_page = st.Page('pages/chain.py', title='Options Chain', icon='📊')
home_page = st.Page('home.py', title='Home', icon='🏠')
strangle_page = st.Page('pages/strangle.py', title='Strangle Visualizer', icon='🏦')
usage_page = st.Page('pages/usage.py', title='Usage', icon='🧠')

pg = st.navigation([home_page, chain_page, strangle_page, usage_page])

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
    - Construct **Strangle** strategies
    - Read the full **Usage Guide**

    ---
    ### 🛡️ Secure API Integration:
    This app is powered by a third-party financial data API. Your API key is stored securely using **Streamlit Secrets**.
    """
)

pg.run()