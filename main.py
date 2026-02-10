from fastapi import FastAPI
from pydantic import BaseModel
import os, importlib.util
from pymongo import MongoClient

app = FastAPI()

# Senin bulduğun gerçek link, şifren eklenmiş haliyle
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/banka_db?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client.banka_veritabani
    hesaplar = db.kullanicilar
    client.admin.command('ping')
    status = "BAGLANDI"
except Exception as e:
    status = f"HATA: {str(e)}"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": status, "Asistan": "Online"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    if "calistir" in metin:
        return {"sonuc": "Factory OS Tetiklendi!", "durum": "Basarili"}
    return {"sonuc": "Komut bekleniyor."}
