from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# DATA FETCH
# -----------------------------

def get_chart_data():
    for i in range(3):
        try:
            data = yf.download("NIFTYBEES.NS", period="1d", interval="5m", timeout=10)
            if not data.empty:
                return data
        except Exception as e:
            print("Retrying...", e)
        time.sleep(2)
    return None


# -----------------------------
# MARKET SNAPSHOT (REAL DATA)
# -----------------------------

def get_market_snapshot():
    data = get_chart_data()

    if data is None or len(data) < 5:
        return None

    close = data["Close"]
    high = data["High"]
    low = data["Low"]
    open_ = data["Open"]
    volume = data["Volume"]

    # Handle multi-column case
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
        high = high.iloc[:, 0]
        low = low.iloc[:, 0]
        open_ = open_.iloc[:, 0]
        volume = volume.iloc[:, 0]

    last_close = float(close.iloc[-1])
    prev_close = float(close.iloc[-5])

    # Trend detection
    if last_close > prev_close:
        trend = "UPTREND"
    elif last_close < prev_close:
        trend = "DOWNTREND"
    else:
        trend = "SIDEWAYS"

    return {
        "nifty": round(last_close * 100),  # convert ETF to index approx
        "open_price": round(float(open_.iloc[0]) * 100),
        "prev_high": round(float(high.tail(10).max()) * 100),
        "prev_low": round(float(low.tail(10).min()) * 100),
        "current_volume": int(volume.iloc[-1]),
        "avg_volume": int(volume.tail(20).mean()),
        "trend": trend,
    }


# -----------------------------
# GREEKS
# -----------------------------

def get_greeks(confidence):
    if confidence > 80:
        return {"delta": 0.6, "theta": -20}
    return {"delta": 0.4, "theta": -35}


# -----------------------------
# ROUTES
# -----------------------------

@app.get("/")
def home():
    return {"status": "Trade AI backend running"}


@app.get("/market")
def market():
    snap = get_market_snapshot()

    if snap is None:
        return {"error": "Market data not available"}

    nifty = snap["nifty"]
    open_price = snap["open_price"]
    prev_high = snap["prev_high"]
    prev_low = snap["prev_low"]
    current_volume = snap["current_volume"]
    avg_volume = snap["avg_volume"]
    chart_trend = snap["trend"]

    momentum = nifty - open_price

    # -----------------------------
    # STRUCTURE
    # -----------------------------

    if nifty > prev_high:
        structure = "BREAKOUT"
    elif nifty < prev_low:
        structure = "BREAKDOWN"
    else:
        structure = "RANGE"

    # -----------------------------
    # VOLUME
    # -----------------------------

    if current_volume > avg_volume * 1.5:
        volume_strength = "HIGH"
    elif current_volume < avg_volume * 0.8:
        volume_strength = "LOW"
    else:
        volume_strength = "NORMAL"

    # -----------------------------
    # MOMENTUM
    # -----------------------------

    if momentum > 40:
        momentum_strength = "STRONG BULLISH"
    elif momentum < -40:
        momentum_strength = "STRONG BEARISH"
    else:
        momentum_strength = "WEAK"

    # -----------------------------
    # DECISION
    # -----------------------------

    if chart_trend == "UPTREND" and volume_strength != "LOW":
        action = "BUY CE"
        entry = nifty
        sl = nifty - 50
        target = nifty + 100
        confidence = 70

    elif structure == "BREAKDOWN" and volume_strength == "HIGH" and chart_trend == "DOWNTREND":
        action = "BUY PE"
        entry = prev_low
        sl = open_price
        target = prev_low - 120
        confidence = 85

    else:
        action = "WAIT"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 40

    # -----------------------------
    # OPTION SELECTION
    # -----------------------------

    strike_step = 50
    atm_strike = round(nifty / strike_step) * strike_step

    if action == "BUY CE":
        option_type = "CE"
        strike = atm_strike
    elif action == "BUY PE":
        option_type = "PE"
        strike = atm_strike
    else:
        option_type = "-"
        strike = "-"

    greeks = get_greeks(confidence)

    # -----------------------------
    # RESPONSE
    # -----------------------------

    return {
        "nifty": str(nifty),
        "structure": structure,
        "volume": volume_strength,
        "momentum": momentum_strength,
        "trend": chart_trend,
        "news": "NEUTRAL",
        "action": action,
        "option_type": option_type,
        "strike": str(strike),
        "entry": str(entry),
        "stop_loss": str(sl),
        "target": str(target),
        "confidence": str(confidence),
        "delta": str(greeks["delta"]),
        "theta": str(greeks["theta"]),
}
