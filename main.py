from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def ana_sayfa():
    return {'Durum': 'Sistem Canavar Gibi Calisiyor'}
