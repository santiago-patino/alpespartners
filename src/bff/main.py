import json
import asyncio
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Any

from .comandos import RegistrarCampaign, ComandoRegistrarCampaign, RegistrarPartner, ComandoRegistrarPartner, RegistrarEvento, ComandoRegistrarEvento, ComandoCancelarCampaign, CancelarCampaign
from .consumidores import suscribirse_a_topico
from .despachadores import Despachador
from typing import Any
from . import utils
import requests
import os

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

@app.post("/registrar-campaign", include_in_schema=False)
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


@app.get("/eliminar-campaign/{id}")
async def eliminar_campaña(id:str) -> Any:
    payload = CancelarCampaign(
        id = id
    )

    comando = ComandoCancelarCampaign(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=CancelarCampaign.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-cancelar-campaign")
    return {"status": "ok"}

ALPESPARTNERS_HOST = os.getenv("ALPESPARTNERS_ADDRESS", default="localhost:8001")
@app.get("/obtener-campaigns")
async def obtener_campaigns() -> Any:
    campaigns_json = requests.get(f'http://{ALPESPARTNERS_HOST}/campaigns').json()
    return campaigns_json

@app.get("/obtener-campaigns/{id}")
async def obtener_campaign(id:str) -> Any:
    campaigns_json = requests.get(f'http://{ALPESPARTNERS_HOST}/campaigns/{id}').json()
    return campaigns_json

class RegistrarPartnerRequest(BaseModel):
    id_campaign: str
    nombre: str
    tipo: str
    informacion_perfil: str

@app.post("/registrar-partner", include_in_schema=False)
async def crear_partner(request: RegistrarPartnerRequest) -> dict[str, str]:
    payload = RegistrarPartner(
        id_campaign = request.id_campaign,  # ID de campaña fijo para la prueba
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

class RegistrarEventoRequest(BaseModel):
    id_partner: str
    id_campana: str
    
@app.post("/registrar-evento", include_in_schema=False)
async def crear_partner(request: RegistrarEventoRequest) -> dict[str, str]:
    payload = RegistrarEvento(
        id_partner = request.id_partner,
        id_campana = request.id_campana,
        fecha = utils.time_millis()
    )

    comando = ComandoRegistrarEvento(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=RegistrarEvento.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-registrar-evento-conversion")
    return {"status": "ok"}