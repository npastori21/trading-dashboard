import streamlit as st
from utils.auth import check_auth
from api.price import get_underlying_price
from display import plot_strangle_payoff

check_auth()
st.set_page_config(page_title="Strangle Strategy", page_icon="🔃")
st.title("🔃 Strangle Strategy Payoff Visualizer")

# --- Inputs ---
with st.form("strangle_form"):
    ticker = st.text_input("Enter the Ticker Symbol", value="NASDAQ:AAPL")
    col1, col2 = st.columns(2)
    with col1:
        put_strike = st.number_input("Put Strike", value=180.0, step=1.0)
        put_premium = st.number_input("Put Premium (per share)", value=2.0, step=0.1)
    with col2:
        call_strike = st.number_input("Call Strike", value=220.0, step=1.0)
        call_premium = st.number_input("Call Premium (per share)", value=2.5, step=0.1)

    quantity = st.number_input("Contracts Sold", value=1, step=1, min_value=1)

    submitted = st.form_submit_button("Visualize Strategy")

# --- Spot Price Fetch + Plot ---
if submitted:
    spot_price = get_underlying_price(ticker.upper())

    if spot_price == 0:
        st.error("⚠️ Could not fetch underlying price. Please check your ticker.")
    else:
        st.info(f"📈 Spot price for {ticker.upper()}: ${spot_price:.2f}")
        fig = plot_strangle_payoff(
            put_strike,
            put_premium,
            call_strike,
            call_premium,
            quantity,
            spot_price
        )
        st.plotly_chart(fig, use_container_width=True)
