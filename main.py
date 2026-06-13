from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import requests
import time


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
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",

        "Accept":
        "application/json",

        "Accept-Language":
        "en-US,en;q=0.9",

        "Referer":
        "https://www.nseindia.com/option-chain"

    }


    try:

        session = requests.Session()


        session.get(
            "https://www.nseindia.com",
            headers=headers,
            timeout=10
        )


        time.sleep(2)



        response = session.get(

            url,

            headers=headers,

            timeout=10

        )



        if response.status_code == 200:

            return response.json()



        print(
            "NSE STATUS:",
            response.status_code
        )


        return None



    except Exception as e:


        print(
            "OPTION ERROR:",
            e
        )


        return None







@app.get("/analyze")
def analyze():



    nifty = yf.Ticker("^NSEI")


    history = nifty.history(
        period="5d"
    )


    price = float(
        history["Close"].iloc[-1]
    )


    previous = float(
        history["Close"].iloc[-2]
    )



    change = price - previous



    atm = atm_strike(price)



    ce_price = 0
    pe_price = 0

    ce_oi = 0
    pe_oi = 0



    ce_trend = "No Data"
    pe_trend = "No Data"


    pcr = 0




    try:


        chain = get_option_chain()



        if chain:


            records = chain.get(
                "records",
                {}
            ).get(
                "data",
                []
            )



            for item in records:



                if item.get("strikePrice") == atm:



                    if "CE" in item:


                        ce = item["CE"]


                        ce_price = ce.get(
                            "lastPrice",
                            0
                        )


                        ce_oi = ce.get(
                            "openInterest",
                            0
                        )




                    if "PE" in item:


                        pe = item["PE"]


                        pe_price = pe.get(
                            "lastPrice",
                            0
                        )


                        pe_oi = pe.get(
                            "openInterest",
                            0
                        )



                    break






            if ce_oi > pe_oi:


                ce_trend = "CE Strong"



            elif pe_oi > ce_oi:


                pe_trend = "PE Strong"





            if ce_oi > 0:


                pcr = round(
                    pe_oi / ce_oi,
                    2
                )




    except Exception as e:


        print(e)







    if change > 0 and pcr < 1:



        signal = "BUY CE"

        confidence = 75




    elif change < 0 and pcr > 1:



        signal = "BUY PE"

        confidence = 75




    else:



        signal = "WAIT"

        confidence = 50







    return {


        "index":
        "NIFTY 50",



        "price":
        round(price,2),



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
        round(price,2),



        "stoploss":
        round(price-80,2),



        "target":
        round(price+120,2)

    }
