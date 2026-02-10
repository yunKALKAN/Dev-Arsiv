from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def ana_sayfa():
    return {"Durum": "SISTEM AKTIF", "Mesaj": "Modüller Yüklenmeye Hazır"}

@app.get("/moduller")
def modulleri_listele():
    liste = os.listdir("./moduller")
    return {"Yuklu_Moduller": liste}
