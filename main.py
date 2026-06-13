from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import requests
import math

app = FastAPI()


@app.get("/")
def home():
    return FileResponse("index.html")


def atm_strike(price):
    return round(price / 50) * 50


def get_option_chain():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent":
        "Mozilla/5.0",
        "Accept":
        "application/json"
    }


    session = requests.Session()

    session.get(
        "https://www.nseindia.com",
        headers=headers
    )


    r = session.get(
        url,
        headers=headers
    )


    return r.json()



@app.get("/analyze")
def analyze():


    # NIFTY DATA

    nifty = yf.Ticker("^NSEI")

    data = nifty.history(period="5d")


    last = float(
        data["Close"].iloc[-1]
    )

    previous = float(
        data["Close"].iloc[-2]
    )


    change = last - previous


    percent = (
        change / previous
    ) * 100



    # OPTION CHAIN

    try:


        option = get_option_chain()


        records = option["records"]["data"]


        atm = atm_strike(last)



        selected = None


        for item in records:

            if item["strikePrice"] == atm:

                selected = item
                break



        ce = selected["CE"]

        pe = selected["PE"]



        ce_price = ce["lastPrice"]

        pe_price = pe["lastPrice"]


        ce_oi = ce["openInterest"]

        pe_oi = pe["openInterest"]



        pcr = round(
            pe_oi / ce_oi,
            2
        )


        if ce_oi > pe_oi:

            option_bias = "CE Strong"

        else:

            option_bias = "PE Strong"



    except Exception as e:


        atm = atm_strike(last)

        ce_price = 0

        pe_price = 0

        ce_oi = 0

        pe_oi = 0

        pcr = 0

        option_bias = "No Data"



    # AI SIGNAL


    if pcr > 1 and change > 0:


        signal = "BUY CE"

        confidence = 75



    elif pcr < 0.8 and change < 0:


        signal = "BUY PE"

        confidence = 75



    else:


        signal = "WAIT"

        confidence = 55




    return {


        "index":"NIFTY 50",


        "price":round(last,2),


        "change":round(change,2),


        "percent":round(percent,2),



        "option_chain":{


            "ATM":atm,


            "CE":{

                "price":ce_price,

                "OI":ce_oi,

                "trend":option_bias

            },


            "PE":{


                "price":pe_price,

                "OI":pe_oi,

                "trend":option_bias

            },


            "PCR":pcr

        },


        "signal":signal,


        "confidence":str(confidence)+"%",



        "entry":round(last,2),


        "stoploss":round(last-80,2),


        "target":round(last+120,2)



    }
