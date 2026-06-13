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

    response = session.get(
        url,
        headers=headers
    )

    return response.json()



@app.get("/analyze")
def analyze():

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



    atm = atm_strike(last)


    ce_price = 0
    pe_price = 0

    ce_oi = 0
    pe_oi = 0

    ce_trend = "No Data"
    pe_trend = "No Data"

    pcr = 0



    try:

        option = get_option_chain()


        records = option["records"]["data"]


        selected = None


        for item in records:

            if item["strikePrice"] == atm:

                selected = item

                break



        if selected:


            ce = selected.get("CE",{})

            pe = selected.get("PE",{})


            ce_price = ce.get(
                "lastPrice",
                0
            )


            pe_price = pe.get(
                "lastPrice",
                0
            )


            ce_oi = ce.get(
                "openInterest",
                0
            )


            pe_oi = pe.get(
                "openInterest",
                0
            )



            if ce_oi > pe_oi:

                ce_trend="CE Strong"

            else:

                pe_trend="PE Strong"



            if ce_oi != 0:

                pcr = round(
                    pe_oi / ce_oi,
                    2
                )



    except Exception as e:

        pass



    # AI LOGIC


    if change > 0 and pcr > 1:

        signal="BUY CE"

        confidence=75


    elif change < 0 and pcr < 1:

        signal="BUY PE"

        confidence=75


    else:

        signal="WAIT"

        confidence=55




    return {


        "index":
        "NIFTY 50",


        "price":
        round(last,2),


        "change":
        round(change,2),


        "percent":
        round(percent,2),



        "option_chain":{


            "ATM":
            atm,


            "CE":{

                "price":
                ce_price,

                "OI":
                ce_oi,

                "trend":
                ce_trend

            },


            "PE":{

                "price":
                pe_price,

                "OI":
                pe_oi,

                "trend":
                pe_trend

            },


            "PCR":
            pcr

        },



        "signal":
        signal,


        "confidence":
        str(confidence)+"%",


        "entry":
        round(last,2),


        "stoploss":
        round(last-80,2),


        "target":
        round(last+120,2)

    }
