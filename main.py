from fastapi import FastAPI
from pydantic import BaseModel
import re, os
from pymongo import MongoClient

app = FastAPI()

# MongoDB Baglantisi - BURAYI KENDI ADRESINLE DEGISTIR
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.kullanici.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client.banka_veritabani
hesaplar = db.kullanicilar

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": "BAGLANDI"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    kullanici = hesaplar.find_one({"id": istek.kullanici_id})
    bakiye = kullanici["bakiye"] if kullanici else 0
    if "bakiye" in metin:
        return {"sonuc": f"Bakiyeniz {bakiye} TL.", "bakiye": bakiye}
    elif "gönder" in metin:
        tutar_bul = re.search(r'(\d+)', metin)
        if tutar_bul:
            miktar = int(tutar_bul.group(1))
            if bakiye >= miktar:
                yeni_bakiye = bakiye - miktar
                hesaplar.update_one({"id": istek.kullanici_id}, {"$set": {"bakiye": yeni_bakiye}}, upsert=True)
                return {"sonuc": f"Başarılı! {miktar} TL gönderildi.", "bakiye": yeni_bakiye}
    return {"sonuc": "Islem anlasilamadi."}
