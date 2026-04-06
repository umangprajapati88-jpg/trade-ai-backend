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
    return {
        "nifty": 22950,
        "banknifty": 48500,
        "pcr": 1.12,
        "iv": 18.5,
        "bias": "NEUTRAL",
        "reason": "OI mixed, no breakout confirmation"
    }
