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
    return {
        "pcr": 1.05,
        "call_oi": 120000000,
        "put_oi": 125000000,
        "bias": "NEUTRAL",
        "note": "Live NSE blocked on cloud, using fallback data"
    }
