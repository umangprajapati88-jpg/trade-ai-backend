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
    # Simulated realistic inputs (we will replace with real API later)
    nifty = 22950
    prev_high = 23020
    prev_low = 22880
    pcr = 1.08
    iv = 17.5

    # Trend logic
    if nifty > prev_high:
        trend = "BREAKOUT BULLISH"
    elif nifty < prev_low:
        trend = "BREAKDOWN BEARISH"
    else:
        trend = "RANGE"

    # Bias logic
    if pcr > 1.3:
        bias = "BULLISH"
    elif pcr < 0.7:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    # Entry logic
    if trend == "BREAKOUT BULLISH":
        entry = f"Buy CE above {prev_high}"
        sl = prev_low
        target = prev_high + 100
        confidence = 75

    elif trend == "BREAKDOWN BEARISH":
        entry = f"Buy PE below {prev_low}"
        sl = prev_high
        target = prev_low - 100
        confidence = 75

    else:
        entry = "Wait for breakout"
        sl = "-"
        target = "-"
        confidence = 40

    return {
        "nifty": nifty,
        "trend": trend,
        "bias": bias,
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence
    }
