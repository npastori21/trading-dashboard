import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Options 101", page_icon="📘")
st.title("📘 Options 101")

st.markdown("""
Welcome to the educational section of **Delta Desk**! Whether you're new to options or need a refresher, this guide covers the basics you need to navigate the platform with confidence.
""")

# Glossary
st.header("🔑 Key Option Terms")
terms = {
    "Call Option": "Gives the buyer the right (not obligation) to **buy** a stock at a strike price before expiration.",
    "Put Option": "Gives the buyer the right (not obligation) to **sell** a stock at a strike price before expiration.",
    "Strike Price": "The fixed price at which the option can be exercised.",
    "Expiration": "The last date on which the option can be exercised.",
    "Premium": "The cost to purchase an option contract.",
    "Implied Volatility (IV)": "Market's expectation of stock volatility over the life of the option.",
    "Delta": "Rate of change of option price with respect to stock price.",
    "Theta": "Rate of time decay in option value.",
    "Gamma": "Rate of change of Delta with respect to stock price.",
    "Vega": "Sensitivity of option price to changes in implied volatility.",
    "Rho": "Sensitivity of option price to changes in interest rates."
}

for term, definition in terms.items():
    with st.expander(term):
        st.write(definition)

# Strategy Examples
st.header("📊 Basic Option Strategies")

strategy_examples = [
    {
        "name": "Strangle",
        "description": "Sell a call above and a put below the current price to profit if the stock stays in range.",
        "call_strike": 110,
        "put_strike": 90,
        "spot_range": (70, 130)
    },
    {
        "name": "Straddle",
        "description": "Sell both a call and a put at the same strike — ideal when expecting low volatility.",
        "call_strike": 100,
        "put_strike": 100,
        "spot_range": (70, 130)
    }
]

def payoff_strangle(S, call_strike, put_strike, premium=5):
    return -np.maximum(S - call_strike, 0) - np.maximum(put_strike - S, 0) + 2 * premium

def render_strategy_chart(name, description, call_strike, put_strike, spot_range):
    st.subheader(f"📈 {name}")
    st.caption(description)
    S = np.linspace(*spot_range, 300)
    payoff = payoff_strangle(S, call_strike, put_strike)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S, y=payoff, mode='lines', name='P/L'))
    fig.update_layout(title=f"{name} Payoff at Expiration", xaxis_title="Stock Price", yaxis_title="Profit / Loss")
    st.plotly_chart(fig, use_container_width=True)

for strat in strategy_examples:
    render_strategy_chart(**strat)