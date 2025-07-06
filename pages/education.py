import streamlit as st
from utils.display import (
    display_covered_call,
    display_cash_sec_put,
    display_long_call,
    display_long_put,
    display_sell_call,
    display_sell_put
)

st.set_page_config(page_title="📘 Options Education", page_icon="📘")
st.title("📘 Options Education")
st.markdown("---")

st.header("📖 Key Terms")

st.markdown("""
Understanding options begins with the fundamentals. Here's a glossary of important terms:

- **Call Option**: The right (but not the obligation) to **buy** an asset at a specific price (strike) before expiration.
- **Put Option**: The right (but not the obligation) to **sell** an asset at a specific price (strike) before expiration.
- **Strike Price**: The price at which the option allows you to buy (call) or sell (put) the underlying asset.
- **Expiration Date**: The last date the option can be exercised.
- **Premium**: The cost to buy an option — paid upfront by the buyer to the seller.
- **Intrinsic Value**: The amount an option is **in-the-money**. For example, if a stock is \\$110 and a call has a strike of \\$100, its intrinsic value is \\$10.
- **Time Value**: The portion of the premium that reflects the time left until expiration.
- **In the Money (ITM)**: When exercising the option would result in a profit.
- **Out of the Money (OTM)**: When exercising the option would result in a loss.
- **Delta**: Sensitivity of the option price to changes in the underlying asset's price.
""")

st.markdown("---")
st.header("🧠 Basic Option Strategies")

st.markdown("""
Below are six foundational strategies in options trading. Each includes a payoff chart and an explanation to help you understand 
the mechanics and risk profiles.
""")

st.subheader("1️⃣ Covered Call")
st.markdown("""
A **covered call** is created by holding a long position in a stock and selling a call option on the same stock. This strategy generates income 
but limits the upside if the stock rallies.
""")
display_covered_call()

st.subheader("2️⃣ Cash-Secured Put")
st.markdown("""
A **cash-secured put** involves selling a put option while holding enough cash to buy the stock at the strike price. It’s a strategy used 
to generate income or acquire stock at a discount.
""")
display_cash_sec_put()

st.subheader("3️⃣ Long Call")
st.markdown("""
A **long call** is a bullish strategy where you buy a call option to profit from a rise in the stock price. Your loss is limited to the 
premium paid, and the upside is theoretically unlimited.
""")
display_long_call()

st.subheader("4️⃣ Long Put")
st.markdown("""
A **long put** is a bearish strategy where you buy a put option to profit from a drop in the stock price. It’s commonly used as a hedge 
or speculative bet against a downturn.
""")
display_long_put()

st.subheader("5️⃣ Naked Call Sell")
st.markdown("""
Selling a **naked call** means selling a call option without owning the underlying stock. This is a high-risk strategy, as losses are 
theoretically unlimited if the stock rallies sharply.
""")
display_sell_call()

st.subheader("6️⃣ Naked Put Sell")
st.markdown("""
Selling a **naked put** is a moderately bullish strategy. You collect a premium and hope the stock stays above the strike. If it falls 
below, you may be obligated to buy the stock at a higher price than market value.
""")
display_sell_put()

st.markdown("---")
st.markdown("© 2025 Nicholas Pastori. All rights reserved.")
