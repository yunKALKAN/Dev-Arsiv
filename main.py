from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import datetime

app = FastAPI()

# Mermi gibi sapan bağlantı
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client.banka_sistemi
cuzdan = db.kullanici_cuzdanlari

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Banka": "BAGLI"}

@app.post("/islem")
def para_bas(istek: Istek):
    # Bankaya (MongoDB) mermiyi sapla
    cuzdan.update_one(
        {"kullanici": "mucizework"},
        {"$inc": {"bakiye": 100}, "$set": {"tarih": datetime.datetime.now()}},
        upsert=True
    )
    res = cuzdan.find_one({"kullanici": "mucizework"})
    return {"Banka_Durumu": "PARA YATIRILDI", "Guncel_Bakiye": res['bakiye']}
