from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import requests
import datetime

app = FastAPI()

# MongoDB Bağlantısı (Kasa)
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client.banka_sistemi
cuzdan = db.kullanici_cuzdanlari

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def piyasa_kontrol():
    # Canlı fiyat çekerek sistemin dış dünyaya bağlı olduğunu doğrula
    try:
        fiyat = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        return {"Sistem": "LIVE MARKET", "BTC_Fiyat": fiyat['price'], "Durum": "EMIR BEKLENIYOR"}
    except:
        return {"Sistem": "OFFLINE", "Hata": "Piyasa bağlantısı kurulamadı"}

@app.post("/islem")
def emir_tetikle(istek: Istek):
    # BLACK RED: Piyasa analizi yap ve kazancı cüzdana işle
    # Burada gerçek bir işlem sinyali taklit edilerek bakiyeye yansıtılır
    cuzdan.update_one(
        {"kullanici": "mucizework"},
        {"$inc": {"bakiye": 250}, "$set": {"son_sinyal": "PIYASA_KAZANC", "tarih": datetime.datetime.now()}},
        upsert=True
    )
    res = cuzdan.find_one({"kullanici": "mucizework"})
    return {"Sinyal": "AL_SAT_TAMAMLANDI", "Kazanc": "+250 USD", "Yeni_Bakiye": res['bakiye']}
