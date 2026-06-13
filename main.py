from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status":"PAN AI Trade Bridge Running"
    }

@app.get("/signal")
def signal():
    return {
        "market":"NIFTY",
        "trend":"Bullish",
        "option":"CE WATCH",
        "confidence":82,
        "analysis":"15 min candle + global cues"
    }
