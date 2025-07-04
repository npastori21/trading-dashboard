import streamlit as st

st.set_page_config(page_title="Usage Guide", page_icon="📘")

st.title("📘 Usage Guide – Delta Desk")

st.markdown("""
Welcome to **Delta Desk**, your one-stop tool for visualizing options strategies and analyzing real-time option chain data. This guide will help you get the most out of each feature on the platform.

---

#### 📊 **Option Chain Viewer**
- Navigate to the **Option Chain Viewer** to:
  - Enter a ticker symbol (e.g., AAPL, TSLA).
  - Define your desired strike price range and interval.
  - Select an expiration date.
  - View cleanly formatted **calls and puts** DataFrames directly from live market data.

---

#### 🔃 **Strangle Strategy Simulator**
- Use this tool to model a **sell strangle** strategy by:
  - Inputting your chosen **put and call strikes**, premiums, and quantity.
  - Viewing an interactive **P&L chart** across a range of underlying prices.
  - Analyzing breakeven points and risk profiles before execution.

---

#### ⚙️ **Platform Features**
- Built with **Streamlit** for interactivity and speed.
- Automatically fetches live prices from the web.
- Keeps your data session-aware — no need to re-enter inputs every time.

---

#### 🛡️ API & Security
- API keys are securely managed via secrets.
- Your usage is private and never shared.

---

Let **Delta Desk** guide your trading analysis — efficiently and visually.
""")
