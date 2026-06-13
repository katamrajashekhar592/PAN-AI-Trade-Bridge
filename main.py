from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf
import requests
import time


app = FastAPI()



@app.get("/")
def home():

    return FileResponse("index.html")





def get_nifty_price():

    try:

        data = yf.Ticker("^NSEI").history(period="2d")


        return float(
            data["Close"].iloc[-1]
        )


    except Exception as e:

        print("PRICE ERROR:",e)

        return 0





def get_atm(price):

    return round(price/50)*50





def get_option_chain():

    try:


        session = requests.Session()



        headers = {


            "User-Agent":

            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",


            "Accept":

            "application/json,text/plain,*/*",


            "Accept-Language":

            "en-US,en;q=0.9",


            "Referer":

            "https://www.nseindia.com/option-chain",


            "Connection":

            "keep-alive"


        }



        home = session.get(

            "https://www.nseindia.com",

            headers=headers,

            timeout=20

        )



        print(
        "HOME STATUS:",
        home.status_code
        )



        time.sleep(2)




        url = (

        "https://www.nseindia.com/api/"
        "option-chain-indices?symbol=NIFTY"

        )



        response = session.get(

            url,

            headers=headers,

            timeout=20

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



        else:


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








@app.get("/analyze")
def analyze():



    price = get_nifty_price()



    atm = get_atm(price)




    ce_price = 0

    pe_price = 0


    ce_oi = 0

    pe_oi = 0




    chain = get_option_chain()





    try:


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

                            "lastPrice",0

                        )



                        ce_oi = item["CE"].get(

                            "openInterest",0

                        )




                    if "PE" in item:



                        pe_price = item["PE"].get(

                            "lastPrice",0

                        )



                        pe_oi = item["PE"].get(

                            "openInterest",0

                        )



                    break





    except Exception as e:


        print(

        "CHAIN ERROR:",

        e

        )







    if ce_oi > 0:


        pcr = round(

            pe_oi / ce_oi,

            2

        )


    else:


        pcr = 0






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






    if ce_price > 0:

        ce_trend = "Active"


    else:

        ce_trend = "Weak"




    if pe_price > 0:

        pe_trend = "Active"


    else:

        pe_trend = "Weak"






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
