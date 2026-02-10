from fastapi import FastAPI
from pydantic import BaseModel
import re, os, importlib
from pymongo import MongoClient

app = FastAPI()

# Kendi gercek linkini buraya yapistir, yoksa veritabani hatasi verir
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.abcde.mongodb.net/banka_db?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    db = client.banka_veritabani
    hesaplar = db.kullanicilar
    client.admin.command('ping')
    status = "BAGLANDI"
except:
    status = "VERITABANI BAGLANTI HATASI"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": status}

@app.post("/islem")
def banka_islemi(istek: Istek):
    return {"sonuc": "Sistem Tetikte, Beyin Aktif"}
