from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import time
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Helpers
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


def get_chart_trend():
    try:
        data = get_chart_data()

        if data is None or len(data) < 5:
            return "SIDEWAYS"

        # ✅ FIX: flatten column
        close = data["Close"]

        # If multi-column → take first column
        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        last = float(close.iloc[-1])
        prev = float(close.iloc[-5])

        if last > prev:
            return "UPTREND"
        elif last < prev:
            return "DOWNTREND"
        else:
            return "SIDEWAYS"

    except Exception as e:
        print("Chart error:", e)
        return "SIDEWAYS"


def get_news_sentiment():
    api_key = "6bfc206c380c48aaa3240656d666283e"
    url = f"https://newsapi.org/v2/everything?q=stock%20market%20india&apiKey={api_key}"

    try:
        response = requests.get(url, timeout=5) # Add timeout
        data = response.json()
        articles = data.get("articles", [])[:10] # Look at more articles

        if not articles:
            return "NEUTRAL"

        score = 0
        # Expanded keywords for better detection
        negative_words = ["crash", "fall", "down", "bear", "sell", "loss", "negative", "drop"]
        positive_words = ["rally", "gain", "up", "bull", "buy", "profit", "positive", "surge"]

        for a in articles:
            title = a.get("title", "").lower()
            if any(word in title for word in negative_words):
                score -= 1
            if any(word in title for word in positive_words):
                score += 1

        if score > 0: return "BULLISH"
        if score < 0: return "BEARISH"
        return "NEUTRAL"
    except Exception as e:
        print(f"News Error: {e}") # This helps you see the error in Render Logs
        return "NEUTRAL"


def get_greeks(confidence):
    if confidence > 80:
        return {"delta": 0.6, "theta": -20}
    else:
        return {"delta": 0.4, "theta": -35}


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"status": "Trade AI backend running"}


@app.get("/market")
def market():

    # 🔹 Real data
    chart_trend = get_chart_trend()
    news_bias = get_news_sentiment()

    # 🔹 Simulated inputs
    nifty = 22950
    open_price = 22920
    prev_high = 23020
    prev_low = 22880

    current_volume = 200000
    avg_volume = 80000

    momentum = 80

    # -----------------------------
    # Logic
    # -----------------------------

    if nifty > prev_high:
        structure = "BREAKOUT"
    elif nifty < prev_low:
        structure = "BREAKDOWN"
    else:
        structure = "RANGE"

    if current_volume > avg_volume * 1.5:
        volume_strength = "HIGH"
    elif current_volume < avg_volume * 0.8:
        volume_strength = "LOW"
    else:
        volume_strength = "NORMAL"

    if momentum > 40:
        momentum_strength = "STRONG BULLISH"
    elif momentum < -40:
        momentum_strength = "STRONG BEARISH"
    else:
        momentum_strength = "WEAK"

    if structure == "BREAKOUT" and volume_strength == "LOW":
        trap = "FAKE BREAKOUT"
    elif structure == "BREAKDOWN" and volume_strength == "LOW":
        trap = "FAKE BREAKDOWN"
    else:
        trap = "VALID"

    # -----------------------------
    # Decision
    # -----------------------------

    if structure == "BREAKOUT" and volume_strength == "HIGH" and news_bias != "BEARISH" and chart_trend == "UPTREND":
        action = "BUY CE"
        entry = prev_high
        sl = open_price
        target = prev_high + 120
        confidence = 85

    elif structure == "BREAKDOWN" and volume_strength == "HIGH" and news_bias != "BULLISH" and chart_trend == "DOWNTREND":
        action = "BUY PE"
        entry = prev_low
        sl = open_price
        target = prev_low - 120
        confidence = 85

    elif trap != "VALID":
        action = "AVOID TRADE"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 30

    else:
        action = "WAIT"
        entry = "-"
        sl = "-"
        target = "-"
        confidence = 40

    # -----------------------------
    # Option Selection
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
    # Final Output
    # -----------------------------

    return {
        "nifty": nifty,
        "structure": structure,
        "volume": volume_strength,
        "momentum": momentum_strength,
        "trend": chart_trend,
        "news": news_bias,
        "action": action,
        "option_type": option_type,
        "strike": strike,
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence,
        "delta": greeks["delta"],
        "theta": greeks["theta"]
    }
