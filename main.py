from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# Para kazanmanı sağlayacak bakiye verileri (Şimdilik geçici, MongoDB gelince oraya akacak)
hesaplar = {"kullanici_1": 5000}

class Istek(BaseModel):
    kullanici_id: str
    metin: str

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Banka_Asistani": "Hazir"}

@app.post("/islem")
def banka_islemi(istek: Istek):
    metin = istek.metin.lower()
    bakiye = hesaplar.get(istek.kullanici_id, 0)
    
    if "bakiye" in metin:
        return {"sonuc": f"Bakiyeniz {bakiye} TL.", "islem_tipi": "bakiye", "bakiye": bakiye}
    
    elif "gönder" in metin:
        tutar_bul = re.search(r'(\d+)', metin)
        if tutar_bul:
            miktar = int(tutar_bul.group(1))
            if bakiye >= miktar:
                hesaplar[istek.kullanici_id] -= miktar
                return {"sonuc": f"Başarılı! {miktar} TL gönderildi.", "islem_tipi": "transfer", "bakiye": hesaplar[istek.kullanici_id]}
            else:
                return {"sonuc": "Yetersiz Bakiye!", "islem_tipi": "hata", "bakiye": bakiye}
    
    return {"sonuc": "Anlaşılamadı.", "islem_tipi": "hata", "bakiye": bakiye}
