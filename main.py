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

    data = yf.Ticker("^NSEI").history(period="5d")

    return float(data["Close"].iloc[-1])




def get_atm(price):

    return round(price / 50) * 50




def get_option_chain():


    try:

        session = requests.Session()


        headers = {

            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",

            "Accept":
            "application/json,text/plain,*/*",

            "Referer":
            "https://www.nseindia.com/option-chain",

            "Connection":
            "keep-alive"

        }



        session.get(
            "https://www.nseindia.com",
            headers=headers,
            timeout=10
        )


        time.sleep(2)



        url = (
            "https://www.nseindia.com/api/"
            "option-chain-indices?symbol=NIFTY"
        )


        response = session.get(
            url,
            headers=headers,
            timeout=10
        )


        if response.status_code == 200:

            return response.json()



        return None



    except Exception as e:

        print("NSE ERROR:",e)

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



    if chain:


        try:


            records = (
                chain
                .get("records", {})
                .get("data", [])
            )



            for item in records:


                if item.get("strikePrice") == atm:


                    if item.get("CE"):


                        ce_price = item["CE"].get(
                            "lastPrice",0
                        )


                        ce_oi = item["CE"].get(
                            "openInterest",0
                        )



                    if item.get("PE"):


                        pe_price = item["PE"].get(
                            "lastPrice",0
                        )


                        pe_oi = item["PE"].get(
                            "openInterest",0
                        )


                    break



        except Exception as e:

            print(e)





    if ce_oi > 0:

        pcr = round(
            pe_oi / ce_oi,
            2
        )

    else:

        pcr = 0





    # AI LOGIC


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


        "index":"NIFTY 50",


        "price":round(price,2),



        "option_chain":{


            "ATM":atm,


            "CE":{


                "price":ce_price,

                "OI":ce_oi,

                "trend":
                "Bullish" if ce_oi > pe_oi else "Weak"

            },


            "PE":{


                "price":pe_price,

                "OI":pe_oi,

                "trend":
                "Bearish" if pe_oi > ce_oi else "Weak"

            },



            "PCR":pcr

        },



        "signal":signal,


        "confidence":confidence,


        "entry":round(price,2),


        "stoploss":round(price-80,2),


        "target":round(price+120,2)



    }
