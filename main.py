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


    price_data = data.history(period="1mo")



    close = price_data["Close"]



    last = float(close.iloc[-1])

    previous = float(close.iloc[-2])


    change = last - previous


    percent = (change / previous) * 100



    # Moving averages

    ma20 = close.rolling(20).mean().iloc[-1]

    ma50 = close.rolling(50).mean().iloc[-1]



    # RSI calculation

    delta = close.diff()


    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)



    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()



    rs = avg_gain / avg_loss


    rsi = 100 - (100/(1+rs))


    rsi_value = float(rsi.iloc[-1])



    # Trend engine


    confidence = 50



    if last > ma20 and last > ma50 and rsi_value > 50:


        trend = "Bullish trend 📈"

        action = "BUY - momentum strong"

        confidence += 25



    elif last < ma20 and last < ma50 and rsi_value < 45:


        trend = "Bearish trend 📉"

        action = "SELL - weakness"

        confidence += 25



    else:


        trend = "Sideways market"

        action = "WAIT - mixed signals"




    # VWAP


    vwap = (
        price_data["Close"] * price_data["Volume"]
    ).sum() / price_data["Volume"].sum()



    if last > vwap:

        market = "Above VWAP - buyers active"

    else:

        market = "Below VWAP - sellers active"




    # Levels


    support = last - (last*0.012)

    resistance = last + (last*0.012)


    stoploss = last - (last*0.004)


    target = last + (last*0.008)




    return {


        "index":"NIFTY50",


        "price":round(last,2),


        "change":round(change,2),


        "percent":round(percent,2),


        "trend":trend,


        "market":market,


        "rsi":round(rsi_value,2),


        "ma20":round(ma20,2),


        "ma50":round(ma50,2),


        "vwap":round(vwap,2),


        "support":round(support,2),


        "resistance":round(resistance,2),


        "confidence":str(min(confidence,95))+"%",


        "stoploss":round(stoploss,2),


        "target":round(target,2),


        "action":action

    }
