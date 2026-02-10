from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = FastAPI()

# Cluster2 ve Örnek Veri Seti Hattı
uri = "mongodb+srv://mucizework:Muzice123!@cluster2.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster2"
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

# Örnek verilerin olduğu veritabanı ve koleksiyon
db = client.sample_supplies
sales = db.sales

@app.get("/")
def ana_sayfa():
    try:
        # Denver'daki son satışı bulalım
        son_satis = sales.find_one({"mağazaKonumu": "Denver"})
        if son_satis:
            musteri_mail = son_satis['müşteri']['e-posta']
            return {
                "Durum": "CLUSTER2 AKTIF", 
                "Veri_Okuma": "BASARILI", 
                "Son_Musteri": musteri_mail
            }
        return {"Durum": "BAGLANDI", "Mesaj": "Veri bulunamadı ama hat açık."}
    except Exception as e:
        return {"Durum": "HATA", "Detay": str(e)}

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Veri tabanıyla entegre işlem yapılıyor."}
