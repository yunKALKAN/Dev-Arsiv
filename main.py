from fastapi import FastAPI
from pydantic import BaseModel
import re, os
from pymongo import MongoClient

app = FastAPI()

# MUCİZE BAĞLANTI: Buradaki URL'yi Atlas'taki gerçek adresinle güncellemen lazım
# Kullanıcı: mucizework | Şifre: Muzice123!
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.abcde.mongodb.net/banka_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client.banka_veritabani
hesaplar = db.kullanicilar

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": "BAGLANDI", "Banka_Asistani": "Online"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    # MongoDB'den kullanıcıyı çekiyoruz
    kullanici = hesaplar.find_one({"id": istek.kullanici_id})
    bakiye = kullanici["bakiye"] if kullanici else 1000  # Yeni gelene 1000 TL hoşgeldin parası
    
    if "bakiye" in metin:
        return {"sonuc": f"Bakiyeniz {bakiye} TL.", "bakiye": bakiye}
    
    elif "gönder" in metin:
        tutar_bul = re.search(r'(\d+)', metin)
        if tutar_bul:
            miktar = int(tutar_bul.group(1))
            if bakiye >= miktar:
                yeni_bakiye = bakiye - miktar
                # Veriyi MongoDB'de kalıcı olarak güncelliyoruz
                hesaplar.update_one({"id": istek.kullanici_id}, {"$set": {"bakiye": yeni_bakiye}}, upsert=True)
                return {"sonuc": f"Başarılı! {miktar} TL gönderildi.", "bakiye": yeni_bakiye}
    
    return {"sonuc": "Anlaşılamadı.", "bakiye": bakiye}
