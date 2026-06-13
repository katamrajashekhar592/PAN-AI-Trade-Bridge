from fastapi import FastAPI
import yfinance as yf

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "PAN AI Trade Bridge Running",
        "version": "2.0"
    }


@app.get("/analyze")
def analyze():

    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")

    price = round(data["Close"].iloc[-1], 2)
    high = round(data["High"].iloc[-1], 2)
    low = round(data["Low"].iloc[-1], 2)

    return {
        "index": "NIFTY50",
        "price": price,
        "day_high": high,
        "day_low": low,
        "trend": "Live data connected",
        "support": low,
        "resistance": high,
        "action": "AI analysis pending"
    }
