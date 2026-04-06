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
    # Simulated market inputs (later real data)
    nifty = 22950
    prev_high = 23020
    prev_low = 22880
    open_price = 22920
    pcr = 1.05
    iv = 17.5

    # Step 1: Market Structure
    if nifty > prev_high:
        structure = "BREAKOUT"
    elif nifty < prev_low:
        structure = "BREAKDOWN"
    else:
        structure = "RANGE"

    # Step 2: Fake Breakout Detection
    if nifty > prev_high and pcr < 0.9:
        trap = "BULL TRAP"
    elif nifty < prev_low and pcr > 1.2:
        trap = "BEAR TRAP"
    else:
        trap = "NO TRAP"

    # Step 3: Bias
    if pcr > 1.3:
        bias = "BULLISH"
    elif pcr < 0.7:
        bias = "BEARISH"
    else:
        bias = "NEUTRAL"

    # Step 4: Entry Logic
    if structure == "BREAKOUT" and trap == "NO TRAP":
        action = "BUY CALL (CE)"
        entry = prev_high
        sl = open_price
        target = prev_high + 120
        confidence = 75

    elif structure == "BREAKDOWN" and trap == "NO TRAP":
        action = "BUY PUT (PE)"
        entry = prev_low
        sl = open_price
        target = prev_low - 120
        confidence = 75

    elif trap != "NO TRAP":
        action = "AVOID TRADE (TRAP DETECTED)"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 30

    else:
        action = "WAIT FOR BREAKOUT"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 40

    return {
        "nifty": nifty,
        "structure": structure,
        "trap": trap,
        "bias": bias,
        "action": action,
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence,
        "reason": f"Structure: {structure}, PCR: {pcr}, Trap: {trap}"
    }
