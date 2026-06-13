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

    df = data.history(period="6mo")


    close = df["Close"]


    last = float(close.iloc[-1])

    previous = float(close.iloc[-2])


    change = last - previous

    percent = (change / previous) * 100



    ma20 = float(close.rolling(20).mean().iloc[-1])

    ma50 = float(close.rolling(50).mean().iloc[-1])



    # RSI

    delta = close.diff()

    gain = delta.where(delta > 0,0)

    loss = -delta.where(delta < 0,0)


    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()


    rs = avg_gain / avg_loss


    rsi = 100 - (100/(1+rs))


    rsi_value = float(rsi.iloc[-1])



    if last > ma20 and rsi_value > 50:

        trend="Bullish trend 📈"

        action="BUY - momentum positive"

        confidence=75


    elif last < ma20 and rsi_value < 45:

        trend="Bearish trend 📉"

        action="SELL - weakness visible"

        confidence=75


    else:

        trend="Sideways market"

        action="WAIT - mixed signals"

        confidence=55




    support = last - 100

    resistance = last + 100


    stoploss = last - 80

    target = last + 120



    return {


        "price":round(last,2),

        "change":round(change,2),

        "percent":round(percent,2),


        "trend":trend,

        "market":"AI analysis active",


        "rsi":round(rsi_value,2),

        "ma20":round(ma20,2),

        "ma50":round(ma50,2),


        "support":round(support,2),

        "resistance":round(resistance,2),


        "confidence":str(confidence)+"%",


        "stoploss":round(stoploss,2),

        "target":round(target,2),


        "action":action

    }
