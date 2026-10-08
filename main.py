import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def yayin_kontrol():
    try:
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        price = btc.get("price")
    except Exception:
        price = None
    return {
        "durum": "arsiv",
        "kasa": "kapali",
        "btc_usdt": price,
        "not": "Piyasa kotasyonu kasa kaniti degildir.",
    }

@app.post("/islem")
def nakit_isle(istek: Istek):
    if not os.environ.get("MONGO_URI"):
        raise HTTPException(status_code=503, detail="MONGO_URI yok. Nakit yazilmadi.")
    raise HTTPException(status_code=402, detail="Odeme kaniti yok. Bakiye artirilmadi.")
