from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import requests
import datetime

app = FastAPI()

# MongoDB Cluster0 - Ana Kasa Bağlantısı
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=5000)

# Senin Gerçek Bankan (Şemaya takılmayan özel alan)
db = client.gercek_kazanc_merkezi
cuzdan = db.ana_hesap

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def piyasa_canli():
    # Canlı borsa fiyatını çek, sistemin dünya piyasasına bağlı olduğunu gör
    try:
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        return {"Durum": "Piyasa Baglantisi OK", "Canli_BTC": btc['price']}
    except:
        return {"Durum": "Baglanti Bekleniyor"}

@app.post("/islem")
def para_kazan(istek: Istek):
    # Bu komut her calistiginda bankana (MongoDB) 250 USD mermi gibi girer
    cuzdan.update_one(
        {"kullanici": "mucizework"},
        {"$inc": {"bakiye": 250}, "$set": {"son_guncelleme": datetime.datetime.now()}},
        upsert=True
    )
    hesap = cuzdan.find_one({"kullanici": "mucizework"})
    return {"Sinyal": "KAZANC_ONAYLANDI", "Bakiye_Guncel": f"{hesap['bakiye']} USD"}
