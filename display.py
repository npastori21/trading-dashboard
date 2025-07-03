import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def home_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        st.page_link("pages/chain.py", label="📊 Option Chain Viewer", icon="📈")
        st.page_link("pages/strangle.py", label="Strangle Strategy", icon="🔃")
        st.page_link("pages/usage.py", label="Usage Guide", icon="📘")

def chain_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        st.page_link("home.py", label="Home", icon="🏠")
        st.page_link("pages/strangle.py", label="Strangle Strategy", icon="🔃")
        st.page_link("pages/usage.py", label="Usage Guide", icon="📘")
        
def usage_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        st.page_link("home.py", label="Home", icon="🏠")
        st.page_link("pages/chain.py", label="📊 Option Chain Viewer", icon="📈")
        st.page_link("pages/strangle.py", label="Strangle Strategy", icon="🔃")

def strangle_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        st.page_link("home.py", label="Home", icon="🏠")
        st.page_link("pages/chain.py", label="📊 Option Chain Viewer", icon="📈")
        st.page_link("pages/usage.py", label="Usage Guide", icon="📘")

def sell_strangle_payoff(sell_put_strike, put_premium, sell_call_strike, call_premium, quantity):
    x = np.linspace(sell_put_strike * 0.75, sell_call_strike * 1.25, 300)
    
    payoff_put = np.minimum(0, x - sell_put_strike) * 100
    payoff_call = np.minimum(0, sell_call_strike - x) * 100

    # Total payoff per contract
    total_payoff = (payoff_put + payoff_call + (put_premium + call_premium) * 100) * quantity

    # Create DataFrame
    df = pd.DataFrame({
        "Stock Price at Expiration": x,
        "Payoff ($)": total_payoff
    })
    
    return df

def plot_strangle_payoff(sell_put_strike, put_premium, sell_call_strike, call_premium, quantity, current_price):
    df = sell_strangle_payoff(
        sell_put_strike, put_premium,
        sell_call_strike, call_premium,
        quantity
    )
    print()
    fig = px.line(
        df,
        x="Stock Price at Expiration",
        y="Payoff ($)",
        title=f"Sell Strangle Payoff (Put @ {sell_put_strike}, Call @ {sell_call_strike})",
    )

    fig.add_hline(y=0, line_dash="dash", line_color="black")
    fig.add_vline(x=current_price, line_dash="dot", line_color="gray", annotation_text="Current Price")

    fig.update_layout(
        xaxis_title="Stock Price at Expiration",
        yaxis_title="Profit / Loss ($)",
        hovermode="x unified",
        template="plotly_white"
    )

    return fig