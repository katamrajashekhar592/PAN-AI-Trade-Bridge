from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "PAN AI Trade Bridge Running",
        "version": "1.0"
    }


@app.get("/analyze")
def analyze():

    return {
        "index": "NIFTY50",
        "trend": "Analyzing",
        "market_view": "AI engine connected",
        "support": "Will calculate",
        "resistance": "Will calculate",
        "global_cues": "Pending",
        "action": "Wait for live data"
    }
