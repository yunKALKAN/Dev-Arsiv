from fastapi import FastAPI
from pydantic import BaseModel
import re, os, importlib.util
from pymongo import MongoClient

app = FastAPI()

# Şifren ve Cluster adınla güncellenmiş gerçek linkin
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/banka_db?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client.banka_veritabani
    hesaplar = db.kullanicilar
    # Bağlantıyı test et
    client.admin.command('ping')
    status = "BAGLANDI"
except Exception as e:
    status = f"BAGLANTI HATASI: {str(e)}"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": status, "Banka_Asistani": "Online"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    if "calistir" in metin:
        return {"sonuc": "Factory OS Aktif!", "durum": "Basarili"}
    return {"sonuc": "Sistem tetikte, komut bekleniyor."}
