from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os, importlib.util

app = FastAPI()

# BLACK: Veritabanı Hattı
uri = "mongodb+srv://mucizework:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    try:
        client.admin.command('ping')
        return {"Durum": "BLACK ACTIVE", "Veritabanı": "BAGLANDI", "Modüller": "Hazır"}
    except:
        return {"Durum": "RED ALERT", "Veritabanı": "HATA"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    
    # MODÜL TETİKLEME MERKEZİ
    modul_haritasi = {
        "calistir": "factory_os_v5",
        "pro": "factory_os_v5_pro",
        "run": "eai_factory_os_local_runner"
    }

    for anahtar, dosya_adi in modul_haritasi.items():
        if anahtar in metin:
            yol = f"moduller/{dosya_adi}.py"
            if os.path.exists(yol):
                try:
                    spec = importlib.util.spec_from_file_location(dosya_adi, yol)
                    m = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(m)
                    return {"sonuc": f"{dosya_adi} ateşlendi!", "durum": "OK"}
                except Exception as e:
                    return {"sonuc": f"Modül Hatası: {str(e)}"}
            return {"sonuc": f"{dosya_adi} bulunamadı!"}

    return {"sonuc": "Komut bekleniyor (calistir/pro/run)"}
