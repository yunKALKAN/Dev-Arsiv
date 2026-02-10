from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = FastAPI()

# Senin bilgilerinle zırhlanmış gerçek bağlantı linki
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Bağlantıyı modern API yapısıyla kuruyoruz
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    try:
        # Kapıyı çal ve bağlantıyı doğrula
        client.admin.command('ping')
        return {
            "Durum": "SISTEM AKTIF", 
            "Veritabanı": "BAGLANDI", 
            "Mesaj": "Dağıtımı işaretledim. MongoDB'ye başarıyla bağlandınız!"
        }
    except Exception as e:
        return {
            "Durum": "SISTEM AKTIF", 
            "Veritabanı": "HATA", 
            "Detay": str(e)
        }

@app.post("/islem")
def banka_islemi(istek: Istek):
    return {"sonuc": "Komut Alındı: " + istek.metin}
