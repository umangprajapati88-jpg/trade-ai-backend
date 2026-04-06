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
    # Simulated inputs (replace with real later)
    nifty = 22950
    open_price = 22920
    prev_high = 23020
    prev_low = 22880

    # Weekly context (simulate last 2-3 weeks)
    weekly_trend = "SIDEWAYS"   # TRENDING / SIDEWAYS
    last_expiry = "VOLATILE"    # TREND / VOLATILE / RANGE

    # Intraday momentum
    momentum = nifty - open_price

    # PCR & IV
    pcr = 1.05
    iv = 17.5

    # Step 1: Structure
    if nifty > prev_high:
        structure = "BREAKOUT"
    elif nifty < prev_low:
        structure = "BREAKDOWN"
    else:
        structure = "RANGE"

    # Step 2: Momentum strength
    if momentum > 40:
        momentum_strength = "STRONG BULLISH"
    elif momentum < -40:
        momentum_strength = "STRONG BEARISH"
    else:
        momentum_strength = "WEAK"

    # Step 3: Expiry risk logic
    if last_expiry == "VOLATILE":
        risk = "HIGH"
    else:
        risk = "NORMAL"

    # Step 4: Final decision logic
    if structure == "BREAKOUT" and momentum_strength == "STRONG BULLISH":
        action = "BUY CE"
        entry = prev_high
        sl = open_price
        target = prev_high + 120
        confidence = 80

    elif structure == "BREAKDOWN" and momentum_strength == "STRONG BEARISH":
        action = "BUY PE"
        entry = prev_low
        sl = open_price
        target = prev_low - 120
        confidence = 80

    elif weekly_trend == "SIDEWAYS":
        action = "LOW CONFIDENCE (SIDEWAYS MARKET)"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 35

    else:
        action = "WAIT"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 40

    return {
        "nifty": nifty,
        "structure": structure,
        "momentum": momentum_strength,
        "weekly_trend": weekly_trend,
        "expiry_behavior": last_expiry,
        "risk_level": risk,
        "action": action,
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence,
        "reason": f"{structure}, {momentum_strength}, Weekly: {weekly_trend}"
    }
