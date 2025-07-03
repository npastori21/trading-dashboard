import streamlit as st
from api import get_underlying_price
from display import plot_strangle_payoff, strangle_sidebar

API_KEY = st.secrets["API_KEY"]

st.set_page_config(page_title="Strangle Strategy", page_icon="🔃")
strangle_sidebar()

st.title("Strangle Strategy Payoff Visualizer")

# Ticker from session state (ensure it's been set previously)
ticker = st.session_state.get("ticker", "")
if not ticker:
    ticker = st.text_input("Enter the Ticker Symbol")
    st.session_state.ticker = ticker

# Input form
put_strike = st.text_input("Enter a Put Strike")
call_strike = st.text_input("Enter a Call Strike")
put_premium = st.text_input("Enter a Put Premium")
call_premium = st.text_input("Enter a Call Premium")
quantity = st.text_input("Enter a Quantity")

# Fetch spot price only if ticker is available
spot_price = None
if st.session_state.ticker:
    spot_price = get_underlying_price(st.session_state.ticker, API_KEY)

# Show chart
if (
    all([
            put_strike, 
            call_strike, 
            put_premium, 
            call_premium, 
            quantity,
            st.button("Generate Payoff Diagram")
        ])
):
    fig = plot_strangle_payoff(
        float(put_strike), float(put_premium),
        float(call_strike), float(call_premium),
        float(quantity),
        spot_price
    )
    st.plotly_chart(fig, use_container_width=True)