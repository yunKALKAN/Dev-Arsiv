from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = FastAPI()

# Küme0 (Cluster0) ve Örnek Mflix Veri Seti Hattı
# Kullanıcı: mucizework | Şifre: Muzice123!
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

# Mflix veritabanına ve filmler koleksiyonuna dalıyoruz
db = client.örnek_mflix
movies = db.movies

@app.get("/")
def ana_sayfa():
    try:
        # Arşivden rastgele bir başyapıt çekelim
        film = movies.find_one({"genres": "Drama"})
        
        return {
            "Durum": "MFLIX AKTIF",
            "Veritabani": "CLUSTER0 BAGLANDI",
            "Film_Arşivi_Boyutu": "83.14 MB",
            "Ornek_Film": film['title'] if film else "Arşiv yükleniyor...",
            "Yıl": film['year'] if film else "-"
        }
    except Exception as e:
        return {"Durum": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Mflix verileri Factory OS modüllerine analiz için aktarıldı."}
