from partner.seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from partner.seedwork.aplicacion.queries import ejecutar_query as query
from dataclasses import dataclass
from .base import ObtenerPartnerBaseHandler
from partner.modulos.infraestructura.repositorios import RepositorioPartners
from partner.modulos.infraestructura.mapeadores import MapeadorPartner
import uuid

@dataclass
class QueryObtenerPartner(Query):
    id: str

class ObtenerPartnerHandler(ObtenerPartnerBaseHandler):

    def handle(self, query: QueryObtenerPartner) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPartners.__class__)
        partner =  self.fabrica_partners.crear_objeto(repositorio.obtener_por_id(query.id), MapeadorPartner())
        return QueryResultado(resultado=partner)

@query.register(QueryObtenerPartner)
def ejecutar_query_obtener_partner(query: QueryObtenerPartner):
    handler = ObtenerPartnerHandler()
    return handler.handle(query)