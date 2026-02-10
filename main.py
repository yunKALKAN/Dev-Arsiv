from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os, importlib.util

app = FastAPI()

# Senin verdiğin mucizework bilgileri ve gerçek Cluster adresin
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Bağlantıyı 5 saniye zaman aşımı ile zırhladık
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        # Veritabanına ping at
        client.admin.command('ping')
        return {"Durum": "SISTEM AKTIF", "Veritabani": "BAGLANDI", "Mesaj": "Bütün bağlantılar yapıldı, sunucu uçuşta!"}
    except Exception as e:
        return {"Durum": "SISTEM AKTIF", "Veritabani": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte, Komut Bekliyor"}
