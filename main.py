from fastapi import FastAPI
from fastapi.responses import FileResponse
import yfinance as yf


app = FastAPI()



@app.get("/")
def home():

    return FileResponse("index.html")




def atm_strike(price):

    return round(price / 50) * 50





def get_option_data(atm):


    try:


        nifty = yf.Ticker("^NSEI")


        expiry = nifty.options[0]


        chain = nifty.option_chain(expiry)



        calls = chain.calls

        puts = chain.puts



        ce_row = calls.iloc[
            (calls["strike"] - atm)
            .abs()
            .argsort()[:1]
        ]



        pe_row = puts.iloc[
            (puts["strike"] - atm)
            .abs()
            .argsort()[:1]
        ]



        ce_price = float(
            ce_row["lastPrice"].values[0]
        )


        ce_oi = int(
            ce_row["openInterest"].values[0]
        )



        pe_price = float(
            pe_row["lastPrice"].values[0]
        )


        pe_oi = int(
            pe_row["openInterest"].values[0]
        )



        if ce_oi > 0:


            pcr = round(
                pe_oi / ce_oi,
                2
            )


        else:

            pcr = 0



        if ce_oi > pe_oi:


            ce_trend = "CE Strong"

            pe_trend = "Weak"


        else:


            ce_trend = "Weak"

            pe_trend = "PE Strong"



        return {


            "ce_price": ce_price,

            "ce_oi": ce_oi,

            "pe_price": pe_price,

            "pe_oi": pe_oi,

            "pcr": pcr,

            "ce_trend": ce_trend,

            "pe_trend": pe_trend

        }



    except Exception as e:


        print(e)



        return {


            "ce_price":0,

            "ce_oi":0,

            "pe_price":0,

            "pe_oi":0,

            "pcr":0,

            "ce_trend":"No Data",

            "pe_trend":"No Data"

        }







@app.get("/analyze")
def analyze():



    nifty = yf.Ticker("^NSEI")



    data = nifty.history(
        period="5d"
    )



    last = float(
        data["Close"].iloc[-1]
    )



    previous = float(
        data["Close"].iloc[-2]
    )



    change = last - previous



    atm = atm_strike(last)



    option = get_option_data(atm)



    ce_price = option["ce_price"]

    pe_price = option["pe_price"]

    ce_oi = option["ce_oi"]

    pe_oi = option["pe_oi"]

    pcr = option["pcr"]



    # AI SIGNAL



    if ce_oi == 0 or pe_oi == 0:


        signal = "WAIT"

        confidence = 50



    elif change > 0 and pcr < 1:


        signal = "BUY CE"

        confidence = 75



    elif change < 0 and pcr > 1:


        signal = "BUY PE"

        confidence = 75



    else:


        signal = "WAIT"

        confidence = 55






    return {


        "index":

        "NIFTY 50",



        "price":

        round(last,2),



        "option_chain":{


            "ATM":

            atm,



            "CE":{


                "price":

                ce_price,


                "OI":

                ce_oi,


                "trend":

                option["ce_trend"]

            },



            "PE":{


                "price":

                pe_price,


                "OI":

                pe_oi,


                "trend":

                option["pe_trend"]

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
