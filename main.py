from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/analyze")
def analyze():

    data = yf.Ticker("^NSEI")

    price = data.history(period="1d")

    last = float(price["Close"].iloc[-1])

    return {
        "index": "NIFTY50",
        "price": last,
        "trend": "Live AI analysis connected",
        "support": last - 50,
        "resistance": last + 50,
        "action": "AI analysis pending"
    }
