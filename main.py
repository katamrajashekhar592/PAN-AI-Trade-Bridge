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

    price = data.history(period="5d")

    last = float(price["Close"].iloc[-1])
    prev = float(price["Close"].iloc[-2])

    change = last - prev


    if change > 0:
        trend = "Bullish trend 📈"
        action = "BUY bias - momentum positive"

    elif change < 0:
        trend = "Bearish trend 📉"
        action = "SELL bias - weakness visible"

    else:
        trend = "Sideways market"
        action = "WAIT - no clear direction"


    confidence = 70 if change > 0 else 40

    stop_loss = last - 80
    target = last + 120


    return {
        "index": "NIFTY50",
        "price": last,
        "trend": trend,
        "support": last - 50,
        "resistance": last + 50,
        "confidence": confidence,
        "stop_loss": stop_loss,
        "target": target,
        "action": action
    }
