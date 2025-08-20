import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG & STYLING ---------------- #
st.set_page_config(page_title="Smart Credit Risk Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS 
st.markdown("""
    <style>
    /* Overall page container and text color */
    .reportview-container {
        background: #121212;
        color: #e0e0e0;
    }
    /* Main content background */
    .css-1d391kg {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    /* Headers and titles */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #bb86fc;
        font-family: 'Inter', sans-serif;
    }
    /* Button styling with a professional glow effect */
    .stButton > button {
        background-color: #03dac6;
        color: #121212;
        border-radius: 8px;
        border: none;
        box-shadow: 0 2px 10px rgba(0, 255, 255, 0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        background-color: #03a89e;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 255, 255, 0.4);
    }
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #2c2c2c;
        color: white;
        border-radius: 8px;
        border: 1px solid #444;
        padding: 10px;
    }
    /* Metric cards styling */
    .stMetric {
        background-color: #2c2c2c;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .stMetric .st-au {
        font-size: 1.5rem;
        font-weight: bold;
        color: #03dac6;
    }
    .stMetric .st-av {
        font-size: 1rem;
        color: #b0b0b0;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2c2c2c;
        color: white !important;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #444;
        margin-bottom: 10px;
    }
    .st-ag {
        border-radius: 10px;
        border: 2px solid #2d3436;
        padding: 10px;
        background-color: #1e1e1e;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("📊 Smart Credit Risk Dashboard")
st.sidebar.markdown("### 🚀 Hackathon Project")
st.sidebar.write("Developed by **Shikhar Gupta**")
st.sidebar.write("📅 August 2025")
st.sidebar.markdown("---")
st.sidebar.info("Analyze stock trends & credit risk with interactive charts and dummy sentiment.")

# ---------------- LANDING SECTION ---------------- #
st.title("💳 Smart Credit Risk Dashboard")
st.markdown("""
Welcome to the **Smart Credit Risk Dashboard** 🎉  
This project analyzes **stock performance**, applies a **dummy credit scoring model**,  
and provides a **visual risk assessment** with interactive charts.  

👉 Enter any stock ticker (Example: `AAPL`, `MSFT`, `TCS.BO`) below to begin.
""")
st.markdown("---")

# ---------------- USER INPUT ---------------- #
st.markdown("### Search for a Ticker")
ticker = st.text_input("🔍 Enter Stock Ticker:", "AAPL").upper()

if ticker:
    try:
        # Show a loading spinner while fetching data
        with st.spinner(f"Fetching data for **{ticker}**..."):
            stock_data = yf.download(ticker, period="1mo", interval="1d")

        if not stock_data.empty:
            # Drop multi-level index and reset for plotting
            stock_data.columns = stock_data.columns.droplevel(1)
            stock_data.reset_index(inplace=True)

            # Calculate price change
            price_change = float(((stock_data["Close"].iloc[-1] - stock_data["Close"].iloc[0]) / stock_data["Close"].iloc[0]) * 100)

            # Dummy sentiment
            neg_news = 0 if price_change > 0 else 2

            # Credit score logic
            score = 100
            if price_change < 0:
                score -= 20
            score -= neg_news * 10

            # Use a collapsible expander for a cleaner layout
            with st.expander(f"📈 View Dashboard for {ticker}", expanded=True):

                # ---------------- METRICS ---------------- #
                st.subheader("Key Metrics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="📉 Price Change (1M)", value=f"{price_change:.2f}%")
                with col2:
                    st.metric(label="📰 Negative News (Dummy)", value=neg_news)
                with col3:
                    st.metric(label="💳 Credit Score", value=score)

                st.markdown("---")

                # ---------------- RISK LEVEL ---------------- #
                st.subheader("⚠️ Risk Level")
                if score > 80:
                    st.success("✅ Low Risk")
                elif 60 < score <= 80:
                    st.warning("⚠️ Moderate Risk")
                else:
                    st.error("❌ High Risk")

                st.markdown("---")

                # ---------------- CHARTS ---------------- #
                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.subheader("📈 Stock Price Trend (1 Month)")
                    fig = px.line(stock_data, x="Date", y="Close", title="Stock Price Trend", template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)

                with col_chart2:
                    st.subheader("📊 News Sentiment (Dummy Data)")
                    sentiments = {
                        "Positive": max(0, 5 + (1 if price_change > 0 else 0)),
                        "Negative": max(0, 2 + (1 if price_change < 0 else 0)),
                        "Neutral": 3,
                    }
                    sentiment_df = pd.DataFrame(list(sentiments.items()), columns=['Sentiment', 'Value'])
                    fig = px.pie(sentiment_df, values='Value', names='Sentiment', title='News Sentiment', template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # ---------------- DATA TABLE ---------------- #
                st.subheader("📌 Stock Metrics (Last 7 Days)")
                st.write(stock_data.tail(7)[["Open", "High", "Low", "Close", "Volume"]])

                st.markdown("---")
                
                # ---------------- HISTORICAL CHART ---------------- #
                st.subheader("📊 Historical Performance (1 Year)")
                hist_data = yf.download(ticker, period="1y", interval="1wk")
                if not hist_data.empty:
                    hist_data.columns = hist_data.columns.droplevel(1)
                    hist_data.reset_index(inplace=True)
                    fig = px.line(hist_data, x="Date", y="Close", title="1-Year Historical Performance", template="plotly_dark")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ No historical data available.")

        else:
            st.error("❌ No stock data found. Try another ticker.")
    except Exception as e:
        st.error(f"❌ An error occurred while fetching data: {e}. Please ensure the ticker symbol is correct.")
