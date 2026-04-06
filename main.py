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

def get_greeks(confidence):
    if confidence > 80:
        return {
            "delta": 0.6,
            "theta": -20
        }
    else:
        return {
            "delta": 0.4,
            "theta": -35
        }

import yfinance as yf

def get_chart_trend():
    data = yf.download("^NSEI", period="1d", interval="5m")

    close = data["Close"]

    if close.iloc[-1] > close.iloc[-5]:
        return "UPTREND"
    elif close.iloc[-1] < close.iloc[-5]:
        return "DOWNTREND"
    else:
        return "SIDEWAYS"

def get_news_sentiment():
    import requests

    api_key = "6bfc206c380c48aaa3240656d666283e"

    url = f"https://newsapi.org/v2/everything?q=stock%20market%20india&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])[:5]

    score = 0

    for a in articles:
        title = a["title"].lower()

        if "crash" in title or "fall" in title:
            score -= 1
        elif "rally" in title or "gain" in title:
            score += 1

    if score > 0:
        return "BULLISH"
    elif score < 0:
        return "BEARISH"
    else:
        return "NEUTRAL"

@app.get("/")
def home():
    return {"status": "Trade AI backend running"}

import requests

import requests

import yfinance as yf
import time

def get_chart_data():
    for i in range(3):
        try:
            data = yf.download(
                "NIFTYBEES.NS",
                period="1d",
                interval="5m",
                timeout=10
            )

            if not data.empty:
                return data

        except Exception as e:
            print("Retrying...", e)

        time.sleep(2)

    return None


def get_chart_trend():
    data = get_chart_data()

    if data is None or len(data) < 5:
        return "UNKNOWN"

    close = data["Close"]

    if close.iloc[-1] > close.iloc[-5]:
        return "UPTREND"
    elif close.iloc[-1] < close.iloc[-5]:
        return "DOWNTREND"
    else:
        return "SIDEWAYS"

@app.get("/market")
def market():
    chart_trend = get_chart_trend()
    
    if chart_trend == "UNKNOWN":
        chart_trend = "SIDEWAYS"
    
    # Simulated inputs
    nifty = 22950
    open_price = 22920
    prev_high = 23020
    prev_low = 22880

    # Volume (simulated)
    current_volume = 120000
    avg_volume = 80000

    # Weekly context
    weekly_trend = "SIDEWAYS"
    last_expiry = "VOLATILE"

    # Momentum
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

    # Step 2: Volume strength
    if current_volume > avg_volume * 1.5:
        volume_strength = "HIGH"
    elif current_volume < avg_volume * 0.8:
        volume_strength = "LOW"
    else:
        volume_strength = "NORMAL"

    # Step 3: Momentum strength
    if momentum > 40:
        momentum_strength = "STRONG BULLISH"
    elif momentum < -40:
        momentum_strength = "STRONG BEARISH"
    else:
        momentum_strength = "WEAK"

    # Step 4: Trap detection (IMPORTANT)
    if structure == "BREAKOUT" and volume_strength == "LOW":
        trap = "FAKE BREAKOUT"
    elif structure == "BREAKDOWN" and volume_strength == "LOW":
        trap = "FAKE BREAKDOWN"
    else:
        trap = "VALID"

    # Step 5: Decision logic
    if (structure == "BREAKOUT" 
        and volume_strength == "HIGH"
        and news_bias != "BEARISH"
        and "BULLISH" in chart_signal):
        action = "BUY CE"
        entry = prev_high
        sl = open_price
        target = prev_high + 120
        confidence = 85

    elif (structure == "BREAKDOWN" 
      and volume_strength == "HIGH"
      and news_bias != "BULLISH"
      and "BEARISH" in chart_signal):
        action = "BUY PE"
        entry = prev_low
        sl = open_price
        target = prev_low - 120
        confidence = 85

    elif trap != "VALID":
        action = "AVOID TRADE (LOW VOLUME TRAP)"
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

    # Step 6: Option Selection Logic

    # Find nearest strike (ATM)
    strike_step = 50
    atm_strike = round(nifty / strike_step) * strike_step

    option_type = "-"
    strike = "-"
    option_style = "-"

    if action == "BUY CE":
        option_type = "CE"

        if confidence >= 80:
            strike = atm_strike
            option_style = "ATM (Safe)"
        else:
            strike = atm_strike + 50
            option_style = "OTM (Aggressive)"

    elif action == "BUY PE":
        option_type = "PE"

        if confidence >= 80:
            strike = atm_strike
            option_style = "ATM (Safe)"
        else:
            strike = atm_strike - 50
            option_style = "OTM (Aggressive)"

    # Step 7: News Sentiment (Simulated for now)

    global_news = "NEGATIVE"   # POSITIVE / NEGATIVE / NEUTRAL
    india_news = "NEUTRAL"

    if global_news == "POSITIVE" and india_news != "NEGATIVE":
        news_bias = "BULLISH"
    elif global_news == "NEGATIVE" and india_news != "POSITIVE":
        news_bias = "BEARISH"
    else:
        news_bias = "MIXED"

    # Step 8: Chart Trend (Simulated)

    trend_5min = "UPTREND"
    trend_1min = "SIDEWAYS"

    if trend_5min == "UPTREND" and trend_1min == "UPTREND":
        chart_signal = "STRONG BULLISH"
    elif trend_5min == "DOWNTREND" and trend_1min == "DOWNTREND":
        chart_signal = "STRONG BEARISH"
    else:
        chart_signal = "WEAK / SIDEWAYS"

        news_bias = get_news_sentiment()
        chart_trend = get_chart_trend()
        greeks = get_greeks(confidence)
    
        return {
        "nifty": nifty,
        "structure": structure,
        "volume_strength": volume_strength,
        "momentum": momentum_strength,
        "trap": trap,
        "action": action,

        "option_type": option_type,
        "strike": strike,
        "option_style": option_style,

        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "confidence": confidence,

        "news_bias": news_bias,
        "chart_trend": chart_trend,
        "delta": greeks["delta"],
        "theta": greeks["theta"],

        "reason": f"{structure}, Volume: {volume_strength}, Momentum: {momentum_strength}"
    }
