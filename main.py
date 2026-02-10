from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import datetime

app = FastAPI()

# Cluster0 - Para Trafiği Hattı
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

# Cüzdan ve İşlem Veritabanı
db = client.banka_sistemi
cuzdan = db.kullanici_cuzdanlari

@app.get("/")
def durum_kontrol():
    try:
        # Mevcut bakiyeyi kontrol et
        hesap = cuzdan.find_one({"kullanici": "mucizework"})
        bakiye = hesap['bakiye'] if hesap else 0
        return {
            "Sistem": "PARA MODULU AKTIF",
            "Kullanici": "mucizework",
            "Mevcut_Bakiye": f"{bakiye} USD",
            "Mesaj": "Sistem tetikte, kazanç için /islem rotasını kullan!"
        }
    except Exception as e:
        return {"Hata": str(e)}

@app.post("/islem")
def para_kazan(istek: BaseModel):
    # OTOMATIK KAZANC TETIKLEYICI
    # Modüllerden gelen analiz sonucunda 100 USD kazanç ekle
    try:
        cuzdan.update_one(
            {"kullanici": "mucizework"},
            {"$inc": {"bakiye": 100}, "$set": {"son_islem": datetime.datetime.now()}},
            upsert=True
        )
        yeni_hesap = cuzdan.find_one({"kullanici": "mucizework"})
        return {
            "Islem": "BASARILI",
            "Kazanc": "+100 USD",
            "Guncel_Bakiye": f"{yeni_hesap['bakiye']} USD",
            "Durum": "Factory OS v5 Pro Görev Tamamlandı"
        }
    except Exception as e:
        return {"Islem": "HATA", "Detay": str(e)}
