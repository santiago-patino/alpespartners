from fastapi import APIRouter, status, BackgroundTasks
from partner.modulos.aplicacion.comandos.registrar_partner import ComandoRegistrarPartner
from partner.seedwork.presentacion.dto import RespuestaAsincrona
from partner.seedwork.aplicacion.comandos import ejecutar_commando
from partner.seedwork.aplicacion.queries import ejecutar_query

from .dto import RegistrarPartner


router = APIRouter()

@router.post("/registrar", status_code=status.HTTP_202_ACCEPTED, response_model=RespuestaAsincrona)
async def registrar_usuario(registrar_partner: RegistrarPartner, background_tasks: BackgroundTasks) -> dict[str, str]:
    comando = ComandoRegistrarPartner(
        nombre=registrar_partner.nombre,
        tipo=registrar_partner.tipo,
        informacion_perfil=registrar_partner.informacion_perfil
        )
    background_tasks.add_task(ejecutar_commando, comando)
    return RespuestaAsincrona(mensaje="Registro de partner en proceso")