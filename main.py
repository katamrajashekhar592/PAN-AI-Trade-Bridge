from fastapi import FastAPI
import yfinance as yf
from datetime import datetime

app = FastAPI(title="PAN AI Trade Bridge")


@app.get("/analyze")
def analyze():

    data = yf.download(
        "^NSEI",
        period="5d",
        interval="15m",
        progress=False
    )

    latest = data.iloc[-1]

    price = float(latest["Close"])
    high = float(data["High"].max())
    low = float(data["Low"].min())

    if price > (high + low) / 2:
        trend = "Bullish"
        action = "BUY"
    else:
        trend = "Bearish"
        action = "SELL"

    return {
        "index": "NIFTY50",
        "live_price": round(price,2),
        "day_high": round(high,2),
        "day_low": round(low,2),
        "trend": trend,
        "action": action,
        "support": round(low,2),
        "resistance": round(high,2),
        "updated": datetime.now().isoformat()
    }
