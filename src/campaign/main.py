from fastapi import FastAPI
from .config.api import app_configs
from .config.db import init_db
from .api.v1.router import router as v1
from contextlib import asynccontextmanager

from .modulos.infraestructura.consumidores import suscribirse_a_topico
from .modulos.infraestructura.v1.eventos import EventoCampaign, CampaignRegistrado
from .modulos.infraestructura.v1.comandos import ComandoRegistrarCampaign, RegistrarCampaign, Participante
from .modulos.infraestructura.despachadores import Despachador
from .modulos.infraestructura import dto
from .seedwork.infraestructura import utils

import json
import asyncio

tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-campaigns", "sub-campaign", EventoCampaign))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-registrar-campaign", "sub-com-registrar-campaign", ComandoRegistrarCampaign))
    tasks.extend([task1, task2])

    yield

    for task in tasks:
        task.cancel()

app = FastAPI(lifespan=lifespan, **app_configs)

@app.get("/prueba-campaign-registrado", include_in_schema=False)
async def prueba_campaign_registrado() -> dict[str, str]:
    lista_participantes = [
        {
            "id": "1",
            "tipo": "influencer",
            "nombre": "Alice Doe",
            "informacion_perfil": "Influencer de moda con 200k seguidores"
        },
    ]
    payload = CampaignRegistrado(
        id = "1232321321", 
        nombre = "Juan",
        presupuesto = 10000,
        divisa = "USD",
        marca_id = "1122E",
        participantes = json.dumps(lista_participantes)
    )

    evento = EventoCampaign(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=CampaignRegistrado.__name__,
        campaign_registrado = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-campaigns")
    return {"status": "ok"}

@app.get("/prueba-registrar-campaign", include_in_schema=False)
async def prueba_registrar_campaign() -> dict[str, str]:
    lista_participantes = [
        {
            "id": "1",
            "tipo": "influencer",
            "nombre": "Alice Doe",
            "informacion_perfil": "Influencer de moda con 200k seguidores"
        },
    ]
    payload = RegistrarCampaign(
        nombre = "Juan",
        presupuesto = 10000,
        divisa = "USD",
        marca_id = "12D12",
        participantes=json.dumps(lista_participantes)
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

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
