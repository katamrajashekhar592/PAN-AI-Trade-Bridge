from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="PAN AI Trade Bridge",
    description="AI based NIFTY50 market analysis API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "status": "PAN AI Trade Bridge is running",
        "time": datetime.now().isoformat()
    }


@app.get("/analyze")
def analyze():

    # Demo AI analysis engine
    # Later we will connect live NIFTY data here

    nifty_analysis = {
        "index": "NIFTY50",
        "trend": "Analyzing",
        "market_view": "AI engine connected",
        "support": [
            "Will calculate support levels"
        ],
        "resistance": [
            "Will calculate resistance levels"
        ],
        "global_cues": "Pending live market connection",
        "action": "WAIT",
        "risk": "Manage with stop loss",
        "timestamp": datetime.now().isoformat()
    }

    return nifty_analysis
