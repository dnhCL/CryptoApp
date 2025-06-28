from fastapi import FastAPI
from core.servicio import obtener_estado_portafolio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crypto Portafolio API", version="1.0")

# Permitir acceso desde cualquier frontend/API cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/estado")
def estado_actual():
    """
    Devuelve el estado actual del portafolio:
    - Datos financieros
    - Análisis técnico por token
    """
    return obtener_estado_portafolio()
