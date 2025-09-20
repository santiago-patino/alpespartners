from traking.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from traking.seedwork.aplicacion.queries import ejecutar_query as query
from traking.modulos.dominio.entidades import Evento

from .base import ObtenerEventoBaseHandler
from traking.modulos.infraestructura.repositorios import RepositorioEventos
from traking.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from traking.config.uow import UnidadTrabajoSQLAlchemy
import uuid

class ObtenerTodosEventos(Query):
    ...

class ObtenerTodosEventosHandler(ObtenerEventoBaseHandler):

    def handle(self, query) -> QueryResultado:
        eventos_dto = []
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)
        
        uow = UnidadTrabajoSQLAlchemy()
        UnidadTrabajoPuerto.set_uow(uow)

        eventos = repositorio.obtener_todos()
        
        eventos_dicts = [evento_a_dict(c) for c in eventos]

        return QueryResultado(resultado=eventos_dicts)
    
@query.register(ObtenerTodosEventos)
def ejecutar_query_obtener_eventos(query: ObtenerTodosEventos):
    handler = ObtenerTodosEventosHandler()
    return handler.handle(query)

def evento_a_dict(evento):

    return {
        "id": str(getattr(evento, "id", "")),
        "id_partner": str(getattr(evento, "id_partner", "")),
        "id_campana": str(getattr(evento, "id_campana", "")),
        "fecha": getattr(evento, "fecha", None)
    }