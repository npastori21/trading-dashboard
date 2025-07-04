import streamlit as st

st.set_page_config(page_title="Usage Guide", layout="wide")
st.title("📘 How to Use Delta Desk")
st.markdown("---")

st.header("🔐 Overview")
st.markdown(
    """
    This app is a multi-page options trading dashboard. It supports both strategy visualization and 
    options chain analysis for customizable strikes, expirations, and premiums.

    You can navigate to different pages using the **sidebar** on the left.
    """
)

st.header("📊 Sell Strangle Payoff Page")
st.markdown(
    """
    This page lets you **visualize the profit/loss** of a short strangle strategy.

    **Inputs:**
    - **Put Strike** – Strike price for the short put
    - **Call Strike** – Strike price for the short call
    - **Put Premium** – Premium received for the short put (per share)
    - **Call Premium** – Premium received for the short call (per share)
    - **Quantity** – Number of contracts (each contract is 100 shares)

    The app displays a **payoff diagram** with:
    - Profit/loss across stock prices
    - Breakeven points
    - Current stock price marker
    """
)

st.header("📈 Chain Page")
st.markdown(
    """
    The **Chain** page pulls real-time options data and lets you filter the chain by strike range and expiration date.

    **Inputs:**
    - **Stock Ticker** – Format: `NYSE:TICKER` (e.g. `NYSE:BBAI`)
    - **Strike Range** – Minimum, maximum, and interval between strikes
    - **Expiration Date** – In `MM-DD-YYYY` format

    After hitting **Refresh Now**, a table will populate showing:
    - Expiration
    - Ask/Bid Prices
    - Black-Scholes prices (historical & implied volatility)
    """
)

st.header("💡 Example Use Case")
st.markdown(
    """
    Want to sell a strangle on `NYSE:BBAI` with:
    - Put @ $6, premium = $0.68
    - Call @ $7, premium = $0.90
    - Quantity = 1 contract

    Just enter the values, and your payoff chart updates automatically.

    Then go to the **Chain page**, enter `NYSE:BBAI`, set strike range from 6 to 9, interval 0.5, pick your 
    expiration, and hit **Refresh**. You'll get bid/ask data and BS estimates.
    """
)

st.info("Check the Home page for a high-level overview and strategy tips.")

