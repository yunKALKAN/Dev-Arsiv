from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# SENİN GERÇEK VE ZIRHLI LİNKİN
uri = "mongodb+srv://mucize%20%C3%A7al%C4%B1%C5%9Fmas%C4%B1:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        client.admin.command('ping')
        return {"Durum": "SISTEM AKTIF", "Veritabani": "BAGLANDI"}
    except Exception as e:
        return {"Durum": "SISTEM AKTIF", "Veritabani": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte, Komut Bekliyor"}
