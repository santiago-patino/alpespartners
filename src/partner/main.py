from fastapi import FastAPI
from partner.config.api import app_configs
from partner.config.db import init_db
from partner.api.v1.router import router as v1
from contextlib import asynccontextmanager

from partner.modulos.infraestructura.consumidores import suscribirse_a_topico
from partner.modulos.infraestructura.v1.eventos import EventoPartner, PartnerRegistrado, TipoPartner
from partner.modulos.infraestructura.v1.comandos import ComandoRegistrarPartner, RegistrarPartner, ComandoCancelarPartner, CancelarPartner
from partner.modulos.infraestructura.v1 import TipoPartner
from partner.modulos.infraestructura.despachadores import Despachador
from partner.seedwork.infraestructura import utils
from partner.modulos.aplicacion.queries.obtener_todos_partners import ObtenerTodosPartners
from partner.modulos.aplicacion.queries.obtener_partner import ObtenerPartner
from partner.seedwork.aplicacion.queries import ejecutar_query

import asyncio
from typing import Any

def importar_modelos_alchemy():
    import partner.modulos.infraestructura.dto
    
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    importar_modelos_alchemy()
    init_db()
    
    # task1 = asyncio.ensure_future(suscribirse_a_topico("evento-partners", "sub-partner", EventoPartner))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-registrar-partner", "sub-com-registrar-partner", ComandoRegistrarPartner))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-cancelar-partner", "sub-com-cancelar-partner", ComandoCancelarPartner))
    tasks.extend([task2, task3])

    yield

    for task in tasks:
        task.cancel()

app = FastAPI(lifespan=lifespan, **app_configs)

@app.get("/prueba-partner-registrado", include_in_schema=False)
async def prueba_partner_registrado() -> dict[str, str]:
    payload = PartnerRegistrado(
        id = "1232321321", 
        nombre = "Juan",
        tipo = TipoPartner.influencer,
        informacion_perfil = "Influencer de moda con 200k seguidores",
        fecha_creacion = utils.time_millis())

    evento = EventoPartner(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=PartnerRegistrado.__name__,
        partner_registrado = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-partners")
    return {"status": "ok"}

@app.get("/prueba-registrar-partner", include_in_schema=False)
async def prueba_registrar_usuario() -> dict[str, str]:
    payload = RegistrarPartner(
        id_campaign = "camp12345",
        nombre = "Juan",
        tipo = TipoPartner.influencer,
        informacion_perfil = "Influencer de moda con 200k seguidores",
        fecha_creacion = utils.time_millis()
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

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/prueba-cancelar-partner", include_in_schema=False)
async def prueba_cancelar_partner() -> dict[str, str]:
    payload = CancelarPartner(
        id = "e0b0ad24-f594-4e4c-b313-bd025fadf6fb"
    )

    comando = ComandoCancelarPartner(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=CancelarPartner.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-cancelar-partner")
    return {"status": "ok"}

@app.get("/partners", include_in_schema=False)
async def obtener_todos_partners() -> Any:
    try:
        query_resultado = ejecutar_query(ObtenerTodosPartners())
        return query_resultado.resultado
    except Exception:
        return {"Status": "No existe"}
    
@app.get("/partners/{id}", include_in_schema=False)
async def obtener_partner(id: str) -> Any:
    try:
        query_resultado = ejecutar_query(ObtenerPartner(id))
        return query_resultado.resultado
    except Exception:
        return {"Status": "No existe"}
    
@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

# app.include_router(v1, prefix="/v1", tags=["Version 1"])
