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

    df = data.history(period="1mo")

    last = float(df["Close"].iloc[-1])
    prev = float(df["Close"].iloc[-2])


    # EMA calculation
    ema20 = df["Close"].ewm(span=20).mean().iloc[-1]
    ema50 = df["Close"].ewm(span=50).mean().iloc[-1]


    # RSI calculation
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.mean()
    avg_loss = loss.mean()

    rsi = 100 - (100 / (1 + (avg_gain / avg_loss)))


    score = 50


    if last > ema20:
        score += 20

    if ema20 > ema50:
        score += 20

    if rsi < 70:
        score += 10


    if score >= 70:
        trend = "Bullish trend 📈"
        action = "BUY bias - momentum positive"

    elif score <= 40:
        trend = "Bearish trend 📉"
        action = "SELL bias - weakness visible"

    else:
        trend = "Sideways market"
        action = "WAIT - no clear direction"


    return {

        "index":"NIFTY50",
        "price":round(last,2),

        "trend":trend,

        "ema20":round(ema20,2),
        "ema50":round(ema50,2),

        "rsi":round(rsi,2),

        "confidence":score,

        "support":round(last-50,2),
        "resistance":round(last+50,2),

        "stop_loss":round(last-80,2),
        "target":round(last+120,2),

        "action":action
    }
