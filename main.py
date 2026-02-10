from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os, importlib.util

app = FastAPI()

# Senin verdiğin URI, şifre 'Muzice123!' ile güncellendi
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Bağlantı Ayarları
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
db = client.banka_veritabani
hesaplar = db.kullanicilar

def veritabani_kontrol():
    try:
        client.admin.command('ping')
        return "BAGLANDI"
    except Exception as e:
        return f"HATA: {str(e)}"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    durum = veritabani_kontrol()
    return {
        "Durum": "SISTEM AKTIF",
        "Veritabani": durum,
        "Mesaj": "Dağıtımı işaretledim. MongoDB'ye başarıyla bağlandınız!" if durum == "BAGLANDI" else "Bağlantı bekleniyor..."
    }

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    if "calistir" in metin:
        return {"sonuc": "Factory OS Tetiklendi!", "durum": "Basarili"}
    return {"sonuc": "Komut bekleniyor."}
