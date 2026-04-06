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

@app.get("/market")
def market():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    records = data["records"]["data"]

    total_ce_oi = 0
    total_pe_oi = 0

    # Calculate total OI
    for item in records:
        if "CE" in item:
            total_ce_oi += item["CE"]["openInterest"]
        if "PE" in item:
            total_pe_oi += item["PE"]["openInterest"]

    # PCR calculation
    pcr = round(total_pe_oi / total_ce_oi, 2)

    # Bias logic
    if pcr > 1.3:
        bias = "BULLISH"
        reason = "High Put OI → strong support"
    elif pcr < 0.7:
        bias = "BEARISH"
        reason = "High Call OI → strong resistance"
    else:
        bias = "NEUTRAL"
        reason = "Balanced OI"

    return {
        "pcr": pcr,
        "total_call_oi": total_ce_oi,
        "total_put_oi": total_pe_oi,
        "bias": bias,
        "reason": reason
    }
