from fastapi import FastAPI
from routers.producto import router as ruta_libros

app = FastAPI()
app.include_router(ruta_libros)

@app.get("/")
def mensaje_inicial():
    return {"mensaje": "hola mundo"}
