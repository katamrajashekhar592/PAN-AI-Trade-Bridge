from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import pandas as pd

app = FastAPI()


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/analyze")
def analyze():

    data = yf.Ticker("^NSEI")

    df = data.history(period="3mo")


    close = df["Close"]


    last = float(close.iloc[-1])
    previous = float(close.iloc[-2])


    change = last - previous
    percent = (change / previous) * 100


    # Moving averages

    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]


    # RSI

    delta = close.diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)


    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()


    rs = avg_gain / avg_loss

    rsi = 100 - (100/(1+rs))

    rsi_value = float(rsi.iloc[-1])


    # Support resistance

    support = float(close.tail(20).min())

    resistance = float(close.tail(20).max())


    # Trend logic

    if last > ma20 and ma20 > ma50 and rsi_value > 55:

        trend = "Bullish trend 📈"
        action = "BUY CE - momentum positive"
        confidence = 75


    elif last < ma20 and ma20 < ma50 and rsi_value < 45:

        trend = "Bearish trend 📉"
        action = "BUY PE - weakness visible"
        confidence = 75


    else:

        trend = "Sideways market"
        action = "WAIT - mixed signals"
        confidence = 55



    # Market type

    if abs(ma20 - ma50) > 100:

        market = "Trending market"


    else:

        market = "Range market"



    stoploss = last - 80

    target = last + 120



    return {

        "index":"NIFTY50",

        "price":round(last,2),

        "change":round(change,2),

        "percent":round(percent,2),

        "trend":trend,

        "market":market,

        "rsi":round(rsi_value,2),

        "ma20":round(float(ma20),2),

        "ma50":round(float(ma50),2),

        "support":round(support,2),

        "resistance":round(resistance,2),

        "confidence":str(confidence)+"%",

        "stoploss":round(stoploss,2),

        "target":round(target,2),

        "action":action

    }
