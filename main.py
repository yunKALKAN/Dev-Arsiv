from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# BLACK: Arka planda sessizce çalışan veritabanı hattı
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        # RED: Eğer bağlantı koparsa burası anında alarm verir
        client.admin.command('ping')
        return {
            "Durum": "BLACK ACTIVE", 
            "Veritabani": "BAGLANDI", 
            "Kod": "Black Red + OK"
        }
    except Exception as e:
        return {
            "Durum": "RED ALERT", 
            "Veritabani": "HATA", 
            "Sebep": str(e)
        }

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte, Komut Bekliyor"}
