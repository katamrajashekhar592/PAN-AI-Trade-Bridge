from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import math

app = FastAPI()


@app.get("/")
def home():
    return FileResponse("index.html")


def get_atm_strike(price):
    return round(price / 50) * 50


@app.get("/analyze")
def analyze():

    # NIFTY DATA
    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="5d")

    last = float(data["Close"].iloc[-1])
    previous = float(data["Close"].iloc[-2])

    change = last - previous
    percent = (change / previous) * 100


    # OPTION DATA
    try:

        option = yf.Ticker("^NSEI")
        expiry = option.options[0]

        chain = option.option_chain(expiry)

        calls = chain.calls
        puts = chain.puts


        atm = get_atm_strike(last)


        ce = calls.iloc[
            (calls["strike"]-atm).abs().argsort()[:1]
        ].iloc[0]


        pe = puts.iloc[
            (puts["strike"]-atm).abs().argsort()[:1]
        ].iloc[0]


        ce_price = float(ce["lastPrice"])
        pe_price = float(pe["lastPrice"])

        ce_oi = int(ce["openInterest"])
        pe_oi = int(pe["openInterest"])


        if ce_price > pe_price:
            ce_trend="Bullish"
            pe_trend="Weak"

        else:
            ce_trend="Weak"
            pe_trend="Bullish"


        pcr = round(pe_oi / ce_oi,2)


    except Exception:

        atm = 0
        ce_price = 0
        pe_price = 0
        ce_oi = 0
        pe_oi = 0
        ce_trend="NA"
        pe_trend="NA"
        pcr=0



    # AI LOGIC

    confidence = 50


    if change > 0 and pcr > 1:

        signal = "BUY CE"
        confidence = 75


    elif change < 0 and pcr < 1:

        signal = "BUY PE"
        confidence = 75


    else:

        signal = "WAIT"
        confidence = 55



    entry = last

    stoploss = last - 80

    target = last + 120



    return {


        "index":"NIFTY 50",

        "price":round(last,2),

        "change":round(change,2),

        "percent":round(percent,2),


        "option_chain":{

            "ATM Strike":atm,


            "CE":{

                "price":ce_price,

                "OI":ce_oi,

                "trend":ce_trend
            },


            "PE":{

                "price":pe_price,

                "OI":pe_oi,

                "trend":pe_trend

            },


            "PCR":pcr
        },


        "confidence":str(confidence)+"%",


        "entry":round(entry,2),

        "stoploss":round(stoploss,2),

        "target":round(target,2),


        "signal":signal

    }
