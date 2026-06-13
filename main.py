from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="PAN AI Trade Bridge",
    description="AI powered NIFTY50 analysis API"
)


@app.get("/")
def home():
    return {
        "status": "PAN AI Trade Bridge running",
        "time": datetime.now().isoformat()
    }


@app.get("/analyze")
def analyze():

    # Current market data (later we connect live NSE feed)
    price = 23622.90
    high = 23645.35
    low = 23313.90

    # Simple AI logic
    if price > (high + low) / 2:
        trend = "Bullish"
        action = "BUY on confirmation"
        confidence = 72
    else:
        trend = "Bearish"
        action = "SELL on confirmation"
        confidence = 68


    support = low
    resistance = high

    stop_loss = round(price - 100, 2)
    target1 = round(price + 150, 2)
    target2 = round(price + 300, 2)


    return {

        "index": "NIFTY50",

        "market_data": {
            "price": price,
            "day_high": high,
            "day_low": low
        },

        "AI_analysis": {

            "trend": trend,

            "action": action,

            "confidence": str(confidence) + "%",

            "support": support,

            "resistance": resistance,

            "trade_plan": {

                "entry": price,

                "stop_loss": stop_loss,

                "target_1": target1,

                "target_2": target2
            }
        },

        "risk_note":
        "Use proper risk management. AI output is for analysis only.",

        "updated":
        datetime.now().isoformat()
    }
