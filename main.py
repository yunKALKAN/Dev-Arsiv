from fastapi import FastAPI
from pydantic import BaseModel
import re, os, importlib
from pymongo import MongoClient

app = FastAPI()

# --- BURAYI DEGISTIRMEZSEN SISTEM ASLA ACILMAZ ---
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@BURAYA_GERCEK_ADRESINI_YAZ.mongodb.net/banka_db?retryWrites=true&w=majority"

try:
    # Artik DNS hatasinda sistem cokmeyecek, sadece hata mesaji verecek
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    db = client.banka_veritabani
    hesaplar = db.kullanicilar
    db_status = "BAGLANDI"
except:
    db_status = "LINK HATALI - KONTROL ET"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": db_status}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    try:
        kullanici = hesaplar.find_one({"id": istek.kullanici_id})
        bakiye = kullanici["bakiye"] if kullanici else 1000
    except:
        return {"sonuc": "Veritabani baglantisi yok."}

    if "bakiye" in metin:
        return {"sonuc": f"Bakiyeniz {bakiye} TL.", "bakiye": bakiye}
    
    if "calistir" in metin:
        try:
            spec = importlib.util.spec_from_file_location("factory_os_v5", "moduller/factory_os_v5.py")
            os_modul = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(os_modul)
            return {"sonuc": "Modul Aktif!", "durum": "Basarili"}
        except:
            return {"sonuc": "Modul yuklenemedi."}
    
    return {"sonuc": "Anlasilamadi."}
