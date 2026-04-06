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
    nifty = 22950
    pcr = 1.12
    iv = 18.5

    if pcr > 1.3:
        bias = "BULLISH"
        reason = "Strong put writing → support forming"
    elif pcr < 0.7:
        bias = "BEARISH"
        reason = "Heavy call writing → resistance forming"
    else:
        bias = "NEUTRAL"
        reason = "No strong direction"

    if bias == "BULLISH":
        entry = "Buy above 22960"
        sl = "22890"
        target = "23080"
        confidence = 65
    elif bias == "BEARISH":
        entry = "Sell below 22900"
        sl = "22970"
        target = "22800"
        confidence = 65
    else:
        entry = "Wait for breakout"
        sl = "-"
        target = "-"
        confidence = 40

    return {
        "nifty": nifty,
        "pcr": pcr,
        "iv": iv,
        "bias": bias,
        "reason": reason,
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence
    }
