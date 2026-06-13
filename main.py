from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import requests
import time


app = FastAPI()



@app.get("/")
def home():

    return FileResponse("index.html")




# -----------------------------
# NIFTY PRICE
# -----------------------------

def get_nifty_price():

    try:

        data = yf.Ticker("^NSEI").history(
            period="2d"
        )

        return float(
            data["Close"].iloc[-1]
        )

    except Exception as e:

        print("PRICE ERROR:",e)

        return 0





# -----------------------------
# ATM STRIKE
# -----------------------------

def get_atm(price):

    return round(price/50)*50





# -----------------------------
# NSE OPTION CHAIN
# -----------------------------

def get_option_chain():

    try:


        session = requests.Session()



        headers = {


            "User-Agent":
            "Mozilla/5.0 (Linux; Android 10)",


            "Accept":
            "application/json",


            "Accept-Language":
            "en-US,en;q=0.9",


            "Referer":
            "https://www.nseindia.com/option-chain",


            "Origin":
            "https://www.nseindia.com"

        }




        session.get(

            "https://www.nseindia.com",

            headers=headers,

            timeout=15

        )



        time.sleep(3)




        response = session.get(


            "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY",


            headers=headers,


            timeout=15

        )



        print(
            "NSE STATUS:",
            response.status_code
        )




        if response.status_code == 200:


            print(
                "OPTION DATA RECEIVED"
            )


            return response.json()




        print(
            "NSE BLOCKED"
        )


        return None




    except Exception as e:


        print(
            "OPTION ERROR:",
            e
        )


        return None







# -----------------------------
# ANALYSIS
# -----------------------------


@app.get("/analyze")
def analyze():



    price = get_nifty_price()



    atm = get_atm(price)



    ce_price = 0

    pe_price = 0


    ce_oi = 0

    pe_oi = 0



    ce_trend = "No Data"

    pe_trend = "No Data"




    try:



        chain = get_option_chain()



        if chain:



            records = (

                chain

                .get("records",{})

                .get("data",[])

            )




            for item in records:



                if item.get("strikePrice") == atm:



                    if "CE" in item:



                        ce_price = item["CE"].get(

                            "lastPrice",
                            0

                        )


                        ce_oi = item["CE"].get(

                            "openInterest",
                            0

                        )



                    if "PE" in item:



                        pe_price = item["PE"].get(

                            "lastPrice",
                            0

                        )


                        pe_oi = item["PE"].get(

                            "openInterest",
                            0

                        )



                    break





    except Exception as e:


        print(
            "ANALYSIS ERROR:",
            e
        )






    # TREND


    if ce_oi > 0:

        ce_trend = "Strong"

    else:

        ce_trend = "Weak"




    if pe_oi > 0:

        pe_trend = "Strong"

    else:

        pe_trend = "Weak"





    # PCR


    if ce_oi > 0:


        pcr = round(

            pe_oi / ce_oi,

            2

        )

    else:


        pcr = 0







    # SIGNAL LOGIC


    if ce_oi == 0 and pe_oi == 0:


        signal = "WAIT"

        confidence = "0%"



    elif pcr > 1.2:


        signal = "BUY PE"

        confidence = "75%"



    elif pcr < 0.8:


        signal = "BUY CE"

        confidence = "75%"



    else:


        signal = "WAIT"

        confidence = "50%"







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
        confidence,




        "entry":
        round(price,2),




        "stoploss":
        round(price-80,2),




        "target":
        round(price+120,2)



    }
