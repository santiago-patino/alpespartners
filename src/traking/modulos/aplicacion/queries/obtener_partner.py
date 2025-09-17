from src.partner.modulos.aplicacion.queries.obtener_partner import QueryObtenerPartner
from ....seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from ....seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import ObtenerEventoBaseHandler
from ....modulos.infraestructura.repositorios import RepositorioEventos
from ....modulos.infraestructura.mapeadores import MapeadorEvento
import uuid

@dataclass
class QueryObtenerEvento(Query):
    id: str

class ObtenerEventoHandler(ObtenerEventoBaseHandler):

    def handle(self, query: QueryObtenerEvento) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)
        evento =  self.fabrica_partners.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorEvento())
        return QueryResultado(resultado=evento)

@query.register(QueryObtenerPartner)
def ejecutar_query_obtener_evento(query: QueryObtenerEvento):
    handler = ObtenerEventoHandler()
    return handler.handle(query)