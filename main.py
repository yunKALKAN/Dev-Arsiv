from fastapi import FastAPI; from pydantic import BaseModel; import re, os, importlib; from pymongo import MongoClient; app = FastAPI(); MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.abcde.mongodb.net/banka_db?retryWrites=true&w=majority"; client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000); db = client.banka_veritabani; hesaplar = db.kullanicilar; @app.get("/")
def ana_sayfa():
    try:
        client.admin.command("ping"); status = "BAGLANDI"
    except:
        status = "HATA"
    return {"Durum": "SISTEM AKTIF", "Veritabani": status}
@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte"}
