import yfinance as yf
import requests

# Replace this with your actual key
NEWS_API_KEY = "6fb638766d2841b88b9ad7151f845bce"

def get_stock_data(ticker="AAPL"):
    """Fetch last 7 days stock price and % change"""
    t = yf.Ticker(ticker)
    hist = t.history(period="7d")
    if hist.empty:
        return None, None
    price_change = (hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0]
    return price_change, hist

def get_news_headlines(query="Apple", max_headlines=5):
    """Fetch latest news"""
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    headlines = [a["title"] for a in response.get("articles", [])[:max_headlines]]
    return headlines

if __name__ == "__main__":
    # ✅ Test: Stock Data
    change, hist = get_stock_data("AAPL")
    print("Stock Change (7d):", change)
    
    # ✅ Test: News Headlines
    news = get_news_headlines("Apple")
    print("Headlines:")
    for n in news:
        print("-", n)


import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------- Step 1: Load raw data ----------
stock_df = pd.read_csv("data/yahoo_stock.csv")
news_df = pd.read_csv("data/news_headlines.csv")

# ---------- Step 2: Clean stock data ----------
# Keep only Date and Close price for simplicity
stock_df = stock_df[["Date", "Close"]]

# Convert Date to proper format
stock_df["Date"] = pd.to_datetime(stock_df["Date"])

# ---------- Step 3: Clean news data ----------
news_df["Date"] = pd.to_datetime(news_df["Date"])
news_df = news_df.dropna()

# ---------- Step 4: Add sentiment to news ----------
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    return score

news_df["Sentiment"] = news_df["Headline"].apply(get_sentiment)

# ---------- Step 5: Aggregate daily sentiment ----------
daily_sentiment = news_df.groupby("Date")["Sentiment"].mean().reset_index()

# ---------- Step 6: Merge stock + sentiment ----------
final_df = pd.merge(stock_df, daily_sentiment, on="Date", how="inner")

# ---------- Step 7: Save processed dataset ----------
final_df.to_csv("data/processed_dataset.csv", index=False)

print("✅ Day 2 complete! Processed dataset saved at data/processed_dataset.csv")

