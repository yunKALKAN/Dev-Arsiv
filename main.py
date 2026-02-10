from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# Kullanıcı adındaki boşluğu (%20) ve özel karakterleri (%C3%A7) kodladık
# Şifren: Muzice123! | Cluster: zeicwx
uri = "mongodb+srv://mucize%20%C3%A7al%C4%B1%C5%9Fmas%C4%B1:Muzice123!@cluster0.zeicwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Bağlantıyı modern API yapısıyla kuruyoruz
client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)

@app.get("/")
def ana_sayfa():
    try:
        # Sunucuya ping atarak bağlantıyı doğrula
        client.admin.command('ping')
        return {
            "Durum": "SISTEM AKTIF",
            "Veritabani": "BAGLANDI",
            "Mesaj": "Dağıtımı işaretledim. MongoDB'ye başarıyla bağlandınız!"
        }
    except Exception as e:
        return {
            "Durum": "SISTEM AKTIF",
            "Veritabani": "HATA",
            "Detay": str(e)
        }

@app.post("/islem")
def banka_islemi(istek: BaseModel):
    return {"sonuc": "Sistem Tetikte, Komut Bekliyor"}
