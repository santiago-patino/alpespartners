from fastapi import FastAPI
from traking.config.api import app_configs
from traking.config.db import init_db
from traking.api.v1.router import router as v1
from contextlib import asynccontextmanager

from traking.modulos.infraestructura.consumidores import suscribirse_a_topico
from traking.modulos.infraestructura.v1.eventos import EventoRegistrado, EventoTraking
from traking.modulos.infraestructura.v1.comandos import ComandoRegistrarEvento, RegistrarEvento, CancelarEvento, ComandoCancelarEvento
from traking.modulos.infraestructura.despachadores import Despachador
from traking.seedwork.infraestructura import utils
from datetime import datetime

import asyncio

def importar_modelos_alchemy():
    import traking.modulos.infraestructura.dto
    
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    importar_modelos_alchemy()
    init_db()
    
    # task1 = asyncio.ensure_future(suscribirse_a_topico("evento-traking", "sub-evento", EventoTraking))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-registrar-evento-conversion", "sub-com-registrar-evento-conversion", ComandoRegistrarEvento))
    task3 = asyncio.ensure_future(suscribirse_a_topico("comando-cancelar-evento", "sub-com-cancelar-evento", ComandoCancelarEvento))
    tasks.extend([task2, task3])

    yield

    for task in tasks:
        task.cancel()

app = FastAPI(lifespan=lifespan, **app_configs)

@app.get("/prueba-evento-registrado", include_in_schema=False)
async def prueba_evento_registrado() -> dict[str, str]:
    payload = EventoRegistrado(
        id = "1232321321", 
        id_partner = "234kjhsdkfseasdf",
        id_campana = "234287bjhnbja",
        fecha = utils.time_millis())

    evento = EventoTraking(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=EventoRegistrado.__name__,
        evento_registrado = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(evento, "evento-traking")
    return {"status": "ok"}

@app.get("/prueba-registrar-evento", include_in_schema=False)
async def prueba_registrar_usuario() -> dict[str, str]:
    
    payload = RegistrarEvento(
        id_partner = "234kjhsdkfseasdf",
        id_campana = "234287bjhnbja",
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

@app.get("/prueba-cancelar-evento", include_in_schema=False)
async def prueba_cancelar_evento() -> dict[str, str]:
    payload = CancelarEvento(
        id = "0bd9855c-2155-4415-9c2b-0df6ca2adf32"
    )

    comando = ComandoCancelarEvento(
        time=utils.time_millis(),
        ingestion=utils.time_millis(),
        datacontenttype=CancelarEvento.__name__,
        data = payload
    )
    despachador = Despachador()
    despachador.publicar_mensaje(comando, "comando-cancelar-evento")
    return {"status": "ok"}

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
