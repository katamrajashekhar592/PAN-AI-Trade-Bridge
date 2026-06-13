from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import yfinance as yf
import math


app = FastAPI()


@app.get("/")
def home():
    return FileResponse("index.html")



def get_option_chain():

    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"


    headers = {

        "User-Agent":
        "Mozilla/5.0",

        "Accept-Language":
        "en-US,en;q=0.9"

    }


    session = requests.Session()


    session.get(
        "https://www.nseindia.com",
        headers=headers
    )


    data = session.get(
        url,
        headers=headers
    ).json()



    return data




@app.get("/analyze")
def analyze():


    # NIFTY PRICE

    nifty = yf.Ticker("^NSEI")

    df = nifty.history(period="5d")


    price = float(
        df["Close"].iloc[-1]
    )



    # ATM STRIKE

    atm = int(
        round(price/50)*50
    )



    # OPTION DATA

    option = get_option_chain()



    records = option["records"]["data"]



    ce = {}

    pe = {}



    for item in records:


        if item["strikePrice"] == atm:


            ce = item.get("CE",{})

            pe = item.get("PE",{})



    ce_ltp = ce.get("lastPrice",0)

    pe_ltp = pe.get("lastPrice",0)


    ce_oi = ce.get("openInterest",0)

    pe_oi = pe.get("openInterest",0)



    if pe_oi !=0:

        pcr = round(
            ce_oi/pe_oi,
            2
        )

    else:

        pcr = 0




    # OPTION AI LOGIC


    if ce_oi > pe_oi and pcr > 1:


        signal="BUY CE"

        confidence=80


        ce_trend="Strong"


        pe_trend="Weak"



    elif pe_oi > ce_oi and pcr < 1:


        signal="BUY PE"

        confidence=80


        ce_trend="Weak"


        pe_trend="Strong"



    else:


        signal="WAIT"


        confidence=55


        ce_trend="Neutral"


        pe_trend="Neutral"




    if signal=="BUY CE":


        entry=ce_ltp

        stop=entry-20

        target=entry+40



    elif signal=="BUY PE":


        entry=pe_ltp

        stop=entry-20

        target=entry+40



    else:


        entry=0

        stop=0

        target=0





    return {


        "nifty":
        round(price,2),


        "atm":
        atm,



        "ce_price":
        ce_ltp,


        "pe_price":
        pe_ltp,



        "ce_oi":
        ce_oi,


        "pe_oi":
        pe_oi,



        "pcr":
        pcr,



        "ce_trend":
        ce_trend,


        "pe_trend":
        pe_trend,



        "signal":
        signal,



        "confidence":
        str(confidence)+"%",



        "entry":
        entry,


        "stoploss":
        stop,


        "target":
        target

    }
