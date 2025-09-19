from fastapi import FastAPI
from campaign.config.api import app_configs
from campaign.config.db import init_db
from campaign.api.v1.router import router as v1
from contextlib import asynccontextmanager

from campaign.modulos.infraestructura.consumidores import suscribirse_a_topico
from campaign.modulos.infraestructura.v1.eventos import EventoCampaign, CampaignRegistradaPayload, EventoPartner
from campaign.modulos.infraestructura.v1.comandos import ComandoRegistrarCampaign, RegistrarCampaign, Participante, ComandoCancelarCampaign, CancelarCampaign
from campaign.modulos.infraestructura.despachadores import Despachador
from campaign.seedwork.infraestructura import utils

from campaign.modulos.sagas.aplicacion import *

import json
import asyncio

def importar_modelos_alchemy():
    import campaign.modulos.infraestructura.dto
    
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    importar_modelos_alchemy()
    init_db()
    
    # task1 = asyncio.ensure_future(suscribirse_a_topico("evento-campaigns", "sub-campaign", EventoCampaign))
    # task2 = asyncio.ensure_future(suscribirse_a_topico("comando-registrar-campaign", "sub-com-registrar-campaign", ComandoRegistrarCampaign))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-cancelar-campaign", "sub-com-cancelar-campaign", ComandoCancelarCampaign))
    task4 = asyncio.ensure_future(suscribirse_a_topico("evento-partners", "sub-partner", EventoPartner))
    tasks.extend([task3, task4])

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
    payload = CampaignRegistradaPayload(
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
        datacontenttype=CampaignRegistradaPayload.__name__,
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

@app.get("/prueba-cancelar-campaign", include_in_schema=False)
async def prueba_registrar_campaign() -> dict[str, str]:
    payload = CancelarCampaign(
        id = "7a21de2b-d521-407a-a21f-93e8158cef52"
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

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
