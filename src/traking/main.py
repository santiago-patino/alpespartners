from fastapi import FastAPI
from .config.api import app_configs
from .config.db import init_db
from .api.v1.router import router as v1
from contextlib import asynccontextmanager

from .modulos.infraestructura.consumidores import suscribirse_a_topico
from .modulos.infraestructura.v1.eventos import EventoRegistrado, EventoTraking
from .modulos.infraestructura.v1.comandos import ComandoRegistrarEvento, RegistrarEvento
from .modulos.infraestructura.despachadores import Despachador
from .seedwork.infraestructura import utils
from datetime import datetime

import asyncio

tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    
    task1 = asyncio.ensure_future(suscribirse_a_topico("evento-traking", "sub-evento", EventoTraking))
    task2 = asyncio.ensure_future(suscribirse_a_topico("comando-registrar-evento-conversion", "sub-com-registrar-evento-conversion", ComandoRegistrarEvento))
    tasks.extend([task1, task2])

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

@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(v1, prefix="/v1", tags=["Version 1"])
