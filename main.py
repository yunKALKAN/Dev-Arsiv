from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# SENİN VERDİĞİN NET BİLGİLERLE GÜNCELLENMİŞ LİNK
# Kullanıcı: mucizework | Şifre: Muzice123! | Cluster: zeicwx
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        # Kapıyı tıkla
        client.admin.command('ping')
        return {"Durum": "SISTEM AKTIF", "Veritabani": "BAGLANDI", "Mesaj": "mucizework girişi başarılı!"}
    except Exception as e:
        return {"Durum": "SISTEM AKTIF", "Veritabani": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte, Komut Bekliyor"}
