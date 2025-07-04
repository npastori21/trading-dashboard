# 📈 Trading Dashboard

A streamlined Streamlit web app for visualizing options strategies and analyzing real-time options chain data. Built for both retail and professional traders looking for fast, interactive insights.

---

## 🚀 Features

- **Sell Strangle Visualizer**  
  Simulate a sell strangle strategy by adjusting strike prices, premiums, and quantities. Visualize P&L across expiration prices using interactive Plotly charts.

- **Real-Time Options Chain**  
  Fetch and explore live market data with customizable expiration dates and strike intervals.

- **Usage Guide**  
  Get detailed help on how to use the platform and interpret strategy results.

- **Secure API Integration**  
  API keys are safely stored using [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management).

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Interactive web UI
- [Plotly](https://plotly.com/python/) – For dynamic, interactive charts
- Python – Data handling and API interaction
- Financial Data API – Live options chain data (via secure API key)

---

## 🧠 Pages

- 🏠 Home – Overview of the dashboard
- 📊 Chain – Live options chain by ticker
- 🏦 Strangle – Build and visualize sell strangle strategy
- 🧠 Usage – Help and usage instructions
