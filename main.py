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

    price_data = data.history(period="5d")

    last = float(price_data["Close"].iloc[-1])
    previous = float(price_data["Close"].iloc[-2])

    change = last - previous

    percent = (change / previous) * 100


    if change > 0:
        trend = "Bullish trend 📈"
        action = "BUY bias - momentum positive"
        confidence = 70

    elif change < 0:
        trend = "Bearish trend 📉"
        action = "SELL bias - weakness visible"
        confidence = 65

    else:
        trend = "Sideways market"
        action = "WAIT - no clear direction"
        confidence = 50


    support = last - 50
    resistance = last + 50

    stoploss = last - 80
    target = last + 120


    return {

        "index": "NIFTY50",

        "price": round(last,2),

        "change": round(change,2),

        "percent": round(percent,2),

        "trend": trend,

        "support": round(support,2),

        "resistance": round(resistance,2),

        "confidence": str(confidence)+"%",

        "stoploss": round(stoploss,2),

        "target": round(target,2),

        "action": action
    }
