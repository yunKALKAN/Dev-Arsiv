from fastapi import FastAPI
import os

app = FastAPI()

# 1. Vitrin (Ana Sayfa)
@app.get("/")
def ana_sayfa():
    return {
        "Durum": "Canlı 🚀",
        "Mesaj": "Banka Asistanı ve Dev Arşiv Hizmete Hazır!",
        "Patron": "yunKALKAN",
        "Belgeler": "/docs adresine giderek sistemi test edebilirsin."
    }

# 2. Depo Sayımı (75 Modülü Listele)
@app.get("/depo")
def dosyalari_listele():
    # Klasördeki tüm dosyaları bulur
    dosyalar = os.listdir(".")
    return {"Mevcut_Moduller": dosyalar}

# 3. Banka Testi (Örnek Fonksiyon)
@app.get("/banka/dolar")
def dolar_tahmin():
    return {"Dolar": "Yükselecek", "Tavsiye": "Yatırım Tavsiyesi Değildir :)"}

