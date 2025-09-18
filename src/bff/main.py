import json
import asyncio
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Any

from .comandos import RegistrarCampaign, ComandoRegistrarCampaign, RegistrarPartner, ComandoRegistrarPartner
from .consumidores import suscribirse_a_topico
from .despachadores import Despachador

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF AlpesParterns"}
app = FastAPI(**app_configs)

class RegistrarCampaignRequest(BaseModel):
    nombre: str
    presupuesto: float
    divisa: str
    marca_id: str
    participantes: list

@app.post("/crear-campaign", include_in_schema=False)
async def crear_campaña(request: RegistrarCampaignRequest) -> dict[str, str]:
    payload = RegistrarCampaign(
        nombre=request.nombre,
        presupuesto=request.presupuesto,
        divisa=request.divisa,
        marca_id=request.marca_id,
        participantes=json.dumps(request.participantes)  # <-- JSON string
    )

    comando = ComandoRegistrarCampaign(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegistrarCampaign.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-registrar-campaign")
    return {"status": "ok"}

class RegistrarPartnerRequest(BaseModel):
    nombre: str
    tipo: str
    informacion_perfil: str

@app.post("/crear-partner", include_in_schema=False)
async def crear_partner(request: RegistrarPartnerRequest) -> dict[str, str]:
    payload = RegistrarPartner(
        nombre = request.nombre,
        tipo = request.tipo,
        informacion_perfil = request.informacion_perfil,
        fecha_creacion = utils.time_millis(),
    )

    comando = ComandoRegistrarPartner(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegistrarPartner.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-registrar-partner")
    return {"status": "ok"}