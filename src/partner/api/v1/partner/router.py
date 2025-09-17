from fastapi import APIRouter, status, BackgroundTasks
from ....modulos.aplicacion.comandos.registrar_partner import ComandoRegistrarPartner
from ....modulos.aplicacion.queries.obtener_partner import QueryObtenerPartner
from ....modulos.infraestructura.mapeadores import MapeadorPartner
from ....seedwork.presentacion.dto import RespuestaAsincrona
from ....seedwork.aplicacion.comandos import ejecutar_commando
from ....seedwork.aplicacion.queries import ejecutar_query

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

@router.get("/{id}")
async def dar_partner_usando_query(id: str):  # o int / UUID, según tu modelo
    if id:
        query_resultado = ejecutar_query(QueryObtenerPartner(id))
        # return query_resultado.resultado.__dict__
        map_partner = MapeadorPartner()
        return map_partner.entidad_a_externo(query_resultado.resultado)
    else:
        return [{'message': 'GET!'}]