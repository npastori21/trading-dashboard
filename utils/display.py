import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from st_aggrid import AgGrid, GridOptionsBuilder

def render_chain_aggrid(chain_df):
    gb = GridOptionsBuilder.from_dataframe(chain_df)

    # Example: Sticky/pinned columns
    gb.configure_column("Strike Price", pinned="left", width=120)

    # Optional: Add sorting, filtering
    gb.configure_default_column(
        filter=True,
        sortable=True,
        resizable=True,
        editable=False
    )


    gb.configure_grid_options(domLayout='autoHeight', suppressHorizontalScroll=False)
    gridOptions = gb.build()
    
    AgGrid(
        chain_df,
        gridOptions=gridOptions,
        height=500,
        theme="streamlit",  # Other themes: 'balham', 'material', 'alpine'
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        fit_columns_on_grid_load=True
    )

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


def bs_d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def bs_d2(S, K, T, r, sigma):
    return bs_d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def calc_delta(S, K, T, r, sigma, option_type):
    d1 = bs_d1(S, K, T, r, sigma)
    if option_type == "call":
        return norm.cdf(d1)
    else:
        return -norm.cdf(-d1)


def calc_gamma(S, K, T, r, sigma):
    d1 = bs_d1(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

def calc_theta(S, K, T, r, sigma, option_type):
    d1 = bs_d1(S, K, T, r, sigma)
    d2 = bs_d2(S, K, T, r, sigma)
    term1 = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))

    if option_type == "call":
        term2 = -r * K * np.exp(-r * T) * norm.cdf(d2)
        return term1 + term2
    else:
        term2 = r * K * np.exp(-r * T) * norm.cdf(-d2)
        return term1 + term2

def create_surface_delta(option_type, K, r, sigma, S_min, S_max):
    S = np.linspace(S_min, S_max, 50)
    T = np.linspace(0.01, 1.0, 50)
    S_grid, T_grid = np.meshgrid(S, T)
    Z = np.zeros_like(S_grid)

    for i in range(len(S)):
        for j in range(len(T)):
            Z[j, i] = calc_delta(S[i], K, T[j], r, sigma, option_type)

    fig = go.Figure(data=[go.Surface(z=Z, x=S, y=T, colorscale='Viridis')])
    fig.update_layout(
        width=900,
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        title="Delta vs Stock Price and Time",
        scene=dict(
            xaxis_title='Stock Price (S)',
            yaxis_title='Time to Expiration (T in years)',
            zaxis_title='Delta',
        )
    )
    return fig

def create_surface_theta(option_type, K, r, sigma, S_min, S_max):
    S = np.linspace(S_min, S_max, 50)
    T = np.linspace(0.01, 1.0, 50)
    S_grid, T_grid = np.meshgrid(S, T)
    Z = np.zeros_like(S_grid)

    for i in range(len(S)):
        for j in range(len(T)):
            Z[j, i] = calc_theta(S[i], K, T[j], r, sigma, option_type)

    fig = go.Figure(data=[go.Surface(z=Z, x=S, y=T, colorscale='Viridis')])
    fig.update_layout(
        width=900,
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        title="Theta vs Stock Price and Time",
        scene=dict(
            xaxis_title='Stock Price (S)',
            yaxis_title='Time to Expiration (T in years)',
            zaxis_title='Delta',
        )
    )
    return fig

def create_surface_gamma(K, r, sigma, S_min, S_max):
    S = np.linspace(S_min, S_max, 50)
    T = np.linspace(0.01, 1.0, 50)
    S_grid, T_grid = np.meshgrid(S, T)
    Z = np.zeros_like(S_grid)

    for i in range(len(S)):
        for j in range(len(T)):
            Z[j, i] = calc_gamma(S[i], K, T[j], r, sigma)

    fig = go.Figure(data=[go.Surface(z=Z, x=S, y=T, colorscale='Viridis')])
    fig.update_layout(
        width=900,
        height=700,
        margin=dict(l=50, r=50, b=50, t=50),
        title="Gamma vs Stock Price and Time",
        scene=dict(
            xaxis_title='Stock Price (S)',
            yaxis_title='Time to Expiration (T in years)',
            zaxis_title='Delta',
        )
    )
    return fig


def _plot_payoff(x, y, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
    fig.update_layout(
        title=title,
        xaxis_title='Stock Price at Expiration',
        yaxis_title='Profit / Loss',
        template='plotly_dark',
        width=700,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)


def display_covered_call():
    S = np.linspace(50, 150, 300)
    strike = 105
    premium = 5
    stock_cost = 100

    # Own the stock
    stock_payoff = S - stock_cost

    # Sell a call
    call_payoff = -np.maximum(S - strike, 0) + premium

    # Total payoff
    total_payoff = stock_payoff + call_payoff

    _plot_payoff(S, total_payoff, "Covered Call Payoff")

def display_cash_sec_put():
    S = np.linspace(50, 150, 300)
    strike = 100
    premium = 5

    # Sell a put
    payoff = np.where(S < strike, -(strike - S) + premium, premium)

    _plot_payoff(S, payoff, "Cash-Secured Put Payoff")


def display_long_call():
    S = np.linspace(50, 150, 300)
    strike = 100
    premium = 5

    payoff = np.maximum(S - strike, 0) - premium
    _plot_payoff(S, payoff, "Long Call Payoff")


def display_long_put():
    S = np.linspace(50, 150, 300)
    strike = 100
    premium = 5

    payoff = np.maximum(strike - S, 0) - premium
    _plot_payoff(S, payoff, "Long Put Payoff")


def display_sell_call():
    S = np.linspace(50, 150, 300)
    strike = 100
    premium = 5

    payoff = np.where(S <= strike, premium, premium - (S - strike))
    _plot_payoff(S, payoff, "Naked Call Sell Payoff")


def display_sell_put():
    S = np.linspace(50, 150, 300)
    strike = 100
    premium = 5

    payoff = np.where(S >= strike, premium, premium - (strike - S))
    _plot_payoff(S, payoff, "Naked Put Sell Payoff")