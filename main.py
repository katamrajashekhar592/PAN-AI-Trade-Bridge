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


    return {
        "index": "NIFTY50",
        "price": last,
        "trend": trend,
        "support": last - 50,
        "resistance": last + 50,
        "action": action
    }
