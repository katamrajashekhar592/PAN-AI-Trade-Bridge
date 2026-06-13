from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from kiteconnect import KiteConnect
import os
import math


app = FastAPI()


# ==========================
# ZERODHA CONFIG
# ==========================

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")


kite = KiteConnect(
    api_key=API_KEY
)


kite.set_access_token(
    ACCESS_TOKEN
)



# ==========================
# MARKET DATA ENGINE
# ==========================

def get_market_data():

    try:


        # NIFTY PRICE

        nifty_data = kite.ltp(
            "NSE:NIFTY 50"
        )


        nifty_price = nifty_data[
            "NSE:NIFTY 50"
        ][
            "last_price"
        ]



        # ATM STRIKE

        atm = int(
            round(nifty_price / 50) * 50
        )



        # CURRENT EXPIRY CHANGE HERE
        expiry = "26JUN"



        ce_symbol = (
            f"NSE:NIFTY{expiry}{atm}CE"
        )


        pe_symbol = (
            f"NSE:NIFTY{expiry}{atm}PE"
        )



        options = kite.ltp(
            [
                ce_symbol,
                pe_symbol
            ]
        )



        ce_price = options.get(
            ce_symbol,
            {}
        ).get(
            "last_price",
            0
        )



        pe_price = options.get(
            pe_symbol,
            {}
        ).get(
            "last_price",
            0
        )



        # PCR LOGIC

        if ce_price > 0:

            pcr = round(
                pe_price / ce_price,
                2
            )

        else:

            pcr = 0



        # AI SIGNAL


        if pcr > 1.2:


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
            nifty_price,


            "option_chain":{


                "ATM":
                atm,


                "CE":{


                    "price":
                    ce_price


                },


                "PE":{


                    "price":
                    pe_price


                }


            },


            "PCR":
            pcr,


            "signal":
            signal,


            "confidence":
            confidence,


            "entry":
            nifty_price,


            "stoploss":
            round(
                nifty_price - 80,
                2
            ),


            "target":
            round(
                nifty_price + 120,
                2
            )

        }



    except Exception as e:


        return {


            "error":
            str(e)

        }





# ==========================
# API ROUTE
# ==========================


@app.get("/analyze")
def analyze():

    return get_market_data()



# ==========================
# DASHBOARD
# ==========================


@app.get("/", response_class=HTMLResponse)
def home():


    data = get_market_data()



    return f"""

<html>

<head>

<title>
PAN AI Trade Bridge
</title>


<style>


body{{

background:#111;
color:white;
font-family:Arial;
text-align:center;

}}


.card{{

background:#222;
padding:30px;
margin:40px;
border-radius:20px;

}}


</style>


</head>



<body>


<h1>
PAN AI Trade Bridge
</h1>


<div class="card">


<h2>
NIFTY 50
</h2>


<h1>
{data.get("price")}
</h1>


<hr>


<h2>
OPTION CHAIN
</h2>


<p>
ATM : {data.get("option_chain",{}).get("ATM")}
</p>


<h3>
CALL CE
</h3>


<p>
Price :
{data.get("option_chain",{}).get("CE",{}).get("price")}
</p>


<h3>
PUT PE
</h3>


<p>
Price :
{data.get("option_chain",{}).get("PE",{}).get("price")}
</p>


<hr>


<h2>
AI SIGNAL :
{data.get("signal")}
</h2>


<p>
Confidence :
{data.get("confidence")}
</p>


<p>
Entry :
{data.get("entry")}
</p>


<p>
Stop Loss :
{data.get("stoploss")}
</p>


<p>
Target :
{data.get("target")}
</p>



<button onclick="location.reload()">

Refresh

</button>


</div>


</body>

</html>


"""
