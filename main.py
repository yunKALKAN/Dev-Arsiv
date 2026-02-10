from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# Yeni Cluster2 linkin (Kullanıcı ve Şifren aynı kalabilir)
uri = "mongodb+srv://mucizework:Muzice123!@cluster2.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2"

client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        client.admin.command('ping')
        return {"Durum": "SISTEM AKTIF", "Veritabanı": "CLUSTER2 BAGLANDI"}
    except Exception as e:
        return {"Durum": "SISTEM AKTIF", "Veritabanı": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Cluster2 Üzerinden Sistem Tetikte"}
