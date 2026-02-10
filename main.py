from fastapi import FastAPI
from pydantic import BaseModel
import re, os, importlib.util
from pymongo import MongoClient

app = FastAPI()

# MongoDB Baglantisi
MONGO_URL = "mongodb+srv://mucizework:Muzice123!@cluster0.abcde.mongodb.net/banka_db?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    db = client.banka_veritabani
    hesaplar = db.kullanicilar
    client.admin.command('ping')
    status = "BAGLANDI"
except:
    status = "BAGLANTI HATASI (DNS/IP)"

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Veritabani": status}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    
    # DINAMIK MODUL YUKLEME (importlib)
    if "calistir" in metin:
        modul_adi = "factory_os_v5" # Burayi dinamiklestirebiliriz
        yol = f"moduller/{modul_adi}.py"
        
        if os.path.exists(yol):
            try:
                spec = importlib.util.spec_from_file_location(modul_adi, yol)
                modul = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modul)
                return {"sonuc": f"{modul_adi} basariyla tetiklendi!", "durum": "OK"}
            except Exception as e:
                return {"sonuc": f"Modul calisma hatasi: {str(e)}"}
        return {"sonuc": "Ilgili modul dosyasi bulunamadi!"}

    return {"sonuc": "Sistem tetikte, komut bekleniyor."}
