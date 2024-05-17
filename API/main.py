from fastapi import FastAPI
from routers.producto import router as ruta_productos

app = FastAPI()
app.include_router(ruta_productos)

@app.get("/")
def mensaje_inicial():
    return {"mensaje": "API PRODUCTOS FERREMAS"}
