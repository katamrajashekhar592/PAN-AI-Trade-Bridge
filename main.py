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

    price_data = data.history(period="3mo")

    close = price_data["Close"]


    last = float(close.iloc[-1])

    previous = float(close.iloc[-2])


    change = last - previous

    percent = (change / previous) * 100



    # Moving averages

    ma20 = float(close.rolling(20).mean().iloc[-1])

    ma50 = float(close.rolling(50).mean().iloc[-1])



    # RSI

    delta = close.diff()

    gain = delta.where(delta > 0,0)

    loss = -delta.where(delta < 0,0)


    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()


    rs = avg_gain / avg_loss


    rsi = float((100 - (100/(1+rs))).iloc[-1])



    # AI Signal Logic


    if last > ma20 and ma20 > ma50 and rsi < 70:

        trend = "Strong Bullish trend 📈"

        action = "BUY bias - momentum positive"

        confidence = 80



    elif last < ma20 and ma20 < ma50 and rsi > 30:

        trend = "Strong Bearish trend 📉"

        action = "SELL bias - weakness visible"

        confidence = 80



    else:

        trend = "Sideways market"

        action = "WAIT - mixed signals"

        confidence = 55




    support = last - 50

    resistance = last + 50


    stoploss = last - 80

    target = last + 120



    return {

        "index":"NIFTY50",

        "price":round(last,2),

        "change":round(change,2),

        "percent":round(percent,2),

        "trend":trend,

        "support":round(support,2),

        "resistance":round(resistance,2),

        "rsi":round(rsi,2),

        "moving_average_20":round(ma20,2),

        "moving_average_50":round(ma50,2),

        "confidence":str(confidence)+"%",

        "stoploss":round(stoploss,2),

        "target":round(target,2),

        "action":action

    }
