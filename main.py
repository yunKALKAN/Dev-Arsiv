from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import datetime

app = FastAPI()
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
db = client.banka_sistemi
cuzdan = db.kullanici_cuzdanlari

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def kontrol():
    res = cuzdan.find_one({"kullanici": "mucizework"})
    return {"Hesap": "mucizework", "Bakiye": res['bakiye'] if res else 0}

@app.post("/islem")
def para_ekle(istek: Istek):
    cuzdan.update_one(
        {"kullanici": "mucizework"},
        {"$inc": {"bakiye": 100}, "$set": {"tarih": datetime.datetime.now()}},
        upsert=True
    )
    return {"islem": "BASARILI", "eklenen": "100 USD"}
