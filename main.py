import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Trade AI backend running"}

import requests

import requests

@app.get("/market")
def market():
    url = "https://api.allorigins.win/raw?url=https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    records = data["records"]["data"]

    total_ce_oi = 0
    total_pe_oi = 0

    for item in records:
        if "CE" in item:
            total_ce_oi += item["CE"]["openInterest"]
        if "PE" in item:
            total_pe_oi += item["PE"]["openInterest"]

    pcr = round(total_pe_oi / total_ce_oi, 2)

    if pcr > 1.3:
        bias = "BULLISH"
    elif pcr < 0.7:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    return {
        "pcr": pcr,
        "call_oi": total_ce_oi,
        "put_oi": total_pe_oi,
        "bias": bias
    }
